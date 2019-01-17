# -*- coding: utf-8 -*-

"""
p2p_parser contains methods for parsing the output files of P2P platforms.

    Each P2P platform has a unique format for presenting investment results.
    The purpose of this module is to provide parser methods to combine them
    into a single output format.

.. moduleauthor:: Niko Sandschneider <nsandschn@gmx.de>

"""

import locale
import pandas as pd
from typing import Union

Parser = Union[
                'bondora', 'dofinance', 'estateguru', 'grupeer', 'iuvo',
                'mintos', 'peerberry', 'robocash', 'swaper', 'twino'
              ]

INTEREST_PAYMENT = 'Zinszahlungen'
BUYBACK_INTEREST_PAYMENT = 'Zinszahlungen aus Rückkäufen'
BUYBACK_PAYMENT = 'Rückkäufe'
INVESTMENT_PAYMENT = 'Investitionen'
REDEMPTION_PAYMENT = 'Tilgungszahlungen'
LATE_FEE_PAYMENT = 'Verzugsgebühren'
INCOMING_PAYMENT = 'Einzahlungen'
OUTGOING_PAYMENT = 'Auszahlungen'
DEFAULT_PAYMENT = 'Ausfälle'
START_BALANCE_NAME = 'Startguthaben'
END_BALANCE_NAME = 'Endsaldo'


def check_missing_cf_types(df, orig_cf_type_name):
    """
    Helper function to identify any unknown cash flow types.

    Args:
        df (pandas.DataFrame): data frame which contains the results for this
        P2P platform
        orig_cf_type_name (str): name of data frame column which contains the
        cash flow types as reported by the P2P platform

    Returns:
        set(str): set consisting of all unknown cash flow types

    """
    return set(df[orig_cf_type_name].where(
        df['Cashflow-Typ'].isna()).dropna().tolist())


def bondora():
    """
    Parser for Bondora.

    Returns:
        list(pandas.DataFrame, set(str)): list with two elements. The first
        element is the data frame containing the parsed results. The second
        element is the set containing all unknown cash flow types.

    """
    df = pd.read_csv('p2p_downloads/bondora_statement.csv', index_col=0)

    df.drop(['Gesamt:'], inplace=True)
    df.replace({'\.': '',  ',': '.',  '€': ''},  inplace=True,  regex=True)
    df.rename_axis('Datum', inplace=True)
    df.rename(
        columns={
            'Eingesetztes Kapital (netto)': INCOMING_PAYMENT,
            'Erhaltene Zinsen - gesamt': INTEREST_PAYMENT,
            'Erhaltener Kapitalbetrag - gesamt': REDEMPTION_PAYMENT,
            'Investitionen (netto)': INVESTMENT_PAYMENT,
        },
        inplace=True
    )
    df.rename(
        columns={
            'Darlehensbetrag und erhaltene Zinsen - insgesamt':
                'Gesamtzahlungen',
            'Geplante Zinsen - gesamt': 'Geplante Zinszahlungen',
            'Geplanter Kapitalbetrag - gesamt': 'Geplante Tilgungszahlungen',
            'Kapitalbetrag und geplante Zinsen - gesamt':
                'Geplante Gesamtzahlungen'
        },
        inplace=True
    )
    df = df.astype('float64')

    df['Währung'] = 'EUR'
    df['Plattform'] = 'Bondora'
    df[DEFAULT_PAYMENT] = (df['Tilgungszahlungen']
                           - df['Geplante Tilgungszahlungen'])

    df.reset_index(level=0, inplace=True)
    # TODO: make sure locale is installed
    locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
    df['Datum'] = pd.to_datetime(df['Datum'], format='%b %Y')
    df['Datum'] = df['Datum'].dt.strftime('%d.%m.%Y')
    df_result = df.set_index(['Plattform', 'Datum', 'Währung'])

    # Since we define the column names, Bondora cannot have missing CF types
    missing_cf_types = set()
    return [df_result, missing_cf_types]


def mintos():
    """
    Parser for Mintos.

    Returns:
        list(pandas.DataFrame, set(str)): list with two elements. The first
        element is the data frame containing the parsed results. The second
        element is the set containing all unknown cash flow types.

    """
    df = pd.read_excel('p2p_downloads/mintos_statement.xlsx')

    if df is None:
        return None

    mintos_dict = dict()
    mintos_dict['Interest income'] = INTEREST_PAYMENT
    mintos_dict['Interest income on rebuy'] = BUYBACK_INTEREST_PAYMENT
    mintos_dict['Delayed interest income on rebuy'] = BUYBACK_INTEREST_PAYMENT
    mintos_dict['Investment principal rebuy'] = BUYBACK_PAYMENT
    mintos_dict['Investment principal increase'] = INVESTMENT_PAYMENT
    mintos_dict['Investment principal repayment'] = REDEMPTION_PAYMENT
    mintos_dict['Late payment fee income'] = LATE_FEE_PAYMENT
    mintos_dict['Incoming client payment'] = INCOMING_PAYMENT
    # Treat bonus/cashback payments as normal interest payments
    mintos_dict['Cashback bonus'] = INTEREST_PAYMENT
    mintos_dict['Reversed incoming client payment'] = OUTGOING_PAYMENT

    df.rename(columns={'Date': 'Datum',  'Currency': 'Währung'},  inplace=True)
    df['Datum'] = pd.to_datetime(df['Datum'])
    df['Datum'] = df['Datum'].dt.strftime('%d.%m.%Y')
    df['Mintos_Cashflow-Typ'], df['Loan ID'] = df['Details'].str.split(
        ' Loan ID: ').str
    df['Mintos_Cashflow-Typ'] = df['Mintos_Cashflow-Typ'].str.split(
        ' Rebuy purpose').str[0]
    df['Cashflow-Typ'] = df['Mintos_Cashflow-Typ'].map(mintos_dict)
    df['Plattform'] = 'Mintos'

    missing_cf_types = check_missing_cf_types(df, 'Mintos_Cashflow-Typ')

    df_result = pd.pivot_table(
        df, values='Turnover',
        index=['Plattform', 'Datum', 'Währung'],
        columns=['Cashflow-Typ'],
        aggfunc=sum
    )
    df_result.fillna(0, inplace=True)

    # TODO: get start and end balance
    # TODO: find better way for handing over missing_cf_types to worker thread

    return [df_result, missing_cf_types]


def robocash():
    """
    Parser for Robocash.

    Returns:
        list(pandas.DataFrame, set(str)): list with two elements. The first
        element is the data frame containing the parsed results. The second
        element is the set containing all unknown cash flow types.

    """
    df = pd.read_excel('p2p_downloads/robocash_statement.xls')

    if df is None:
        return None

    robocash_dict = dict()
    robocash_dict['Zinsenzahlung'] = INTEREST_PAYMENT
    robocash_dict['Darlehenskauf'] = INVESTMENT_PAYMENT
    robocash_dict['Kreditrückzahlung'] = REDEMPTION_PAYMENT
    robocash_dict['Die Geldauszahlung'] = OUTGOING_PAYMENT
    robocash_dict['Geldeinzahlung'] = INCOMING_PAYMENT

    df = df[df.Operation != 'Die Geldauszahlung aus dem Portfolio']
    df = df[df.Operation != 'Portfolio auffüllen']
    df.rename(columns={'Datum und Laufzeit': 'Datum'},  inplace=True)
    df['Datum'] = pd.to_datetime(df['Datum'],  format='%Y-%m-%d %H:%M:%S')
    df['Datum'] = df['Datum'].dt.strftime('%d.%m.%Y')
    df['Cashflow-Typ'] = df['Operation'].map(robocash_dict)
    df['Währung'] = 'EUR'
    df['Plattform'] = 'Robocash'

    missing_cf_types = check_missing_cf_types(df, 'Operation')

    df_result = pd.pivot_table(
        df, values='Betrag',
        index=['Plattform', 'Datum', 'Währung'],
        columns=['Cashflow-Typ'],
        aggfunc=sum
    )
    df_result.fillna(0, inplace=True)

    return [df_result, missing_cf_types]


def swaper():
    """
    Parser for Swaper.

    Returns:
        list(pandas.DataFrame, set(str)): list with two elements. The first
        element is the data frame containing the parsed results. The second
        element is the set containing all unknown cash flow types.

    """
    df = pd.read_excel('p2p_downloads/swaper_statement.xlsx')

    if df is None:
        return None

    swaper_dict = dict()
    swaper_dict['REPAYMENT_INTEREST'] = INTEREST_PAYMENT
    swaper_dict['EXTENSION_INTEREST'] = INTEREST_PAYMENT
    swaper_dict['INVESTMENT'] = INVESTMENT_PAYMENT
    swaper_dict['REPAYMENT_PRINCIPAL'] = REDEMPTION_PAYMENT
    swaper_dict['BUYBACK_INTEREST'] = BUYBACK_INTEREST_PAYMENT
    swaper_dict['BUYBACK_PRINCIPAL'] = BUYBACK_PAYMENT

    df.rename(columns={'Booking date': 'Datum'},  inplace=True)
    df['Datum'] = df['Datum'].dt.strftime('%d.%m.%Y')
    df['Cashflow-Typ'] = df['Transaction type'].map(swaper_dict)
    df['Währung'] = 'EUR'
    df['Plattform'] = 'Swaper'

    missing_cf_types = check_missing_cf_types(df, 'Transaction type')

    df_result = pd.pivot_table(
        df, values='Amount',
        index=['Plattform', 'Datum', 'Währung'],
        columns=['Cashflow-Typ'],
        aggfunc=sum
    )
    df_result.fillna(0, inplace=True)

    return [df_result, missing_cf_types]


def peerberry():
    """
    Parser for Peerberry.

    Returns:
        list(pandas.DataFrame, set(str)): list with two elements. The first
        element is the data frame containing the parsed results. The second
        element is the set containing all unknown cash flow types.

    """
    df = pd.read_csv('p2p_downloads/peerberry_statement.csv')

    if df is None:
        return None

    peerberry_dict = dict()
    peerberry_dict['Amount of interest payment received'] = INTEREST_PAYMENT
    peerberry_dict['Investment'] = INVESTMENT_PAYMENT
    peerberry_dict['Amount of principal payment received'] = REDEMPTION_PAYMENT

    df.rename(
        columns={'Date': 'Datum', 'Currency Id': 'Währung'}, inplace=True)
    df['Datum'] = pd.to_datetime(df['Datum'],  format='%Y-%m-%d')
    df['Datum'] = df['Datum'].dt.strftime('%d.%m.%Y')
    df['Cashflow-Typ'] = df['Type'].map(peerberry_dict)
    df['Plattform'] = 'Peerberry'

    missing_cf_types = check_missing_cf_types(df, 'Type')

    df_result = pd.pivot_table(
        df, values='Amount',
        index=['Plattform', 'Datum', 'Währung'],
        columns=['Cashflow-Typ'],
        aggfunc=sum
    )
    df_result.fillna(0, inplace=True)

    return [df_result, missing_cf_types]


def estateguru():
    """
    Parser for Estateguru.

    Returns:
        list(pandas.DataFrame, set(str)): list with two elements. The first
        element is the data frame containing the parsed results. The second
        element is the set containing all unknown cash flow types.

    """
    df = pd.read_csv('p2p_downloads/estateguru_statement.csv')

    if df is None:
        return None

    estateguru_dict = dict()
    estateguru_dict['Zins'] = INTEREST_PAYMENT
    # Treat bonus payments as normal interest payments
    estateguru_dict['Bonus'] = INTEREST_PAYMENT
    estateguru_dict['Investition(Auto Investieren)'] = INVESTMENT_PAYMENT
    estateguru_dict['Hauptbetrag'] = REDEMPTION_PAYMENT
    estateguru_dict['Einzahlung(Banktransfer)'] = INCOMING_PAYMENT
    estateguru_dict['Entschädigung'] = LATE_FEE_PAYMENT

    df = df[:-1]  # Drop last line which only contains a summary
    df.rename(
        columns={
            'Zahlungsdatum': 'Datum',
            'Cashflow-Typ': 'Estateguru_Cashflow-Typ',
        }, inplace=True)

    df['Datum'] = pd.to_datetime(df['Datum'],  format='%d/%m/%Y %H:%M')
    df['Datum'] = df['Datum'].dt.strftime('%d.%m.%Y')
    df['Cashflow-Typ'] = df['Estateguru_Cashflow-Typ'].map(estateguru_dict)
    df['Plattform'] = 'Estateguru'
    df['Währung'] = 'EUR'
    df['Betrag'] = df['Betrag'].astype('float')

    missing_cf_types = check_missing_cf_types(df, 'Estateguru_Cashflow-Typ')

    df_result = pd.pivot_table(
        df, values='Betrag',
        index=['Plattform', 'Datum', 'Währung'],
        columns=['Cashflow-Typ'],
        aggfunc=sum
    )
    df_result.fillna(0, inplace=True)

    return [df_result, missing_cf_types]


def iuvo():
    """
    Parser for Iuvo.

    Returns:
        list(pandas.DataFrame, set(str)): list with two elements. The first
        element is the data frame containing the parsed results. The second
        element is the set containing all unknown cash flow types.

    """
    df = pd.read_csv('p2p_downloads/iuvo_statement.csv')

    if df is None:
        return None

    df[INTEREST_PAYMENT] = 0
    df[REDEMPTION_PAYMENT] = 0
    # Date column will raise an error which can be ignored:
    df = df.astype('float64', errors='ignore')

    interest_types = ['Zins erhalten', 'Vorzeitige Zinstilgung']
    for it in interest_types:
        if it in df.columns:
            df[INTEREST_PAYMENT] += df[it]
            del df[it]

    redemption_types = [
        'Vorzeitige Kreditbetragtilgung', 'Kreditbetrag erhalten']
    for rt in redemption_types:
        if rt in df.columns:
            df[REDEMPTION_PAYMENT] += df[rt]
            del df[rt]

    df.rename(
        columns={
            'Anfangsbestand': START_BALANCE_NAME,
            'Automatische Kapitalanlage auf dem Primärmarkt':
                INVESTMENT_PAYMENT,
            'Endbestand': END_BALANCE_NAME,
            'Kreditbetrag bei Rückkauf erhalten': BUYBACK_PAYMENT,
            'Verzugsstrafen erhalten': LATE_FEE_PAYMENT
        }, inplace=True)
    df['Datum'] = pd.to_datetime(df['Datum'], format='%d.%m.%Y')
    df['Datum'] = df['Datum'].dt.strftime('%d.%m.%Y')
    df['Plattform'] = 'Iuvo'
    df['Währung'] = 'EUR'

    df.reset_index(level=0, inplace=True)
    df_result = df.set_index(['Plattform', 'Datum', 'Währung'])

    # Since we set the column names, there cannot be unknown CF types
    missing_cf_types = set()
    return [df_result, missing_cf_types]


def grupeer():
    """
    Parser for Grupeer.

    Returns:
        list(pandas.DataFrame, set(str)): list with two elements. The first
        element is the data frame containing the parsed results. The second
        element is the set containing all unknown cash flow types.

    """
    df = pd.read_excel('p2p_downloads/grupeer_statement.xlsx')

    if df is None:
        return None

    grupeer_dict = dict()
    grupeer_dict['Interest'] = INTEREST_PAYMENT
    grupeer_dict['Investment'] = INVESTMENT_PAYMENT
    grupeer_dict['Deposit'] = INCOMING_PAYMENT
    # Treat cashback as interest payment:
    grupeer_dict['Cashback'] = INTEREST_PAYMENT
    grupeer_dict['Principal'] = REDEMPTION_PAYMENT

    df.rename(columns={'Date': 'Datum'}, inplace=True)
    df['Datum'] = pd.to_datetime(df['Datum'],  format="%d.%m.%Y")
    df['Datum'] = df['Datum'].dt.strftime('%d.%m.%Y')
    df['Cashflow-Typ'] = df['Type'].map(grupeer_dict)
    df['Plattform'] = 'Grupeer'
    df['Währung'] = 'EUR'
    df['Amount'] = df['Amount'].apply(lambda x: x.replace(',', '.')).astype(
        'float')

    missing_cf_types = check_missing_cf_types(df, 'Type')

    df_result = pd.pivot_table(
        df, values='Amount',
        index=['Plattform', 'Datum', 'Währung'],
        columns=['Cashflow-Typ'],
        aggfunc=sum
    )
    df_result.fillna(0, inplace=True)

    return [df_result, missing_cf_types]


def dofinance():
    """
    Parser for Dofinance.

    Returns:
        list(pandas.DataFrame, set(str)): list with two elements. The first
        element is the data frame containing the parsed results. The second
        element is the set containing all unknown cash flow types.

    """
    df = pd.read_excel('p2p_downloads/dofinance_statement.xlsx')

    if df is None:
        return None

    dofinance_dict = dict()
    dofinance_dict['Verdienter Gewinn'] = INTEREST_PAYMENT
    dofinance_dict['Auszahlung auf Bankkonto'] = OUTGOING_PAYMENT
    dofinance_dict[
        'Abgeschlossene Investition\nRate: 12% Typ: automatisch'] = \
        REDEMPTION_PAYMENT
    dofinance_dict['Anlage\nRate: 12% Typ: automatisch'] = INVESTMENT_PAYMENT

    df = df[:-2]  # drop the last two rows
    df.rename(columns={'Bearbeitungsdatum': 'Datum'}, inplace=True)
    df['Datum'] = pd.to_datetime(df['Datum'],  format='%d.%m.%Y')
    df['Datum'] = df['Datum'].dt.strftime('%d.%m.%Y')
    df['Cashflow-Typ'] = df['Art der Transaktion'].map(dofinance_dict)
    df['Plattform'] = 'DoFinance'
    df['Währung'] = 'EUR'

    missing_cf_types = check_missing_cf_types(df, 'Art der Transaktion')

    df_result = pd.pivot_table(
        df, values='Betrag, €',
        index=['Plattform', 'Datum', 'Währung'],
        columns=['Cashflow-Typ'],
        aggfunc=sum
    )
    df_result.fillna(0, inplace=True)

    return [df_result, missing_cf_types]


def twino():
    """
    Parser for Twino.

    Returns:
        list(pandas.DataFrame, set(str)): list with two elements. The first
        element is the data frame containing the parsed results. The second
        element is the set containing all unknown cash flow types.

    """
    df = pd.read_excel('p2p_downloads/twino_statement.xlsx')

    if df is None:
        return None

    twino_dict = dict()
    twino_dict['EXTENSION INTEREST'] = INTEREST_PAYMENT
    twino_dict['REPAYMENT INTEREST'] = INTEREST_PAYMENT
    twino_dict['SCHEDULE INTEREST'] = INTEREST_PAYMENT
    twino_dict['BUYBACK INTEREST'] = BUYBACK_INTEREST_PAYMENT
    twino_dict['REPURCHASE INTEREST'] = BUYBACK_INTEREST_PAYMENT
    twino_dict['BUYBACK PRINCIPAL'] = BUYBACK_PAYMENT
    twino_dict['REPURCHASE PRINCIPAL'] = BUYBACK_PAYMENT
    twino_dict['REPAYMENT PRINCIPAL'] = REDEMPTION_PAYMENT
    twino_dict['BUY_SHARES PRINCIPAL'] = INVESTMENT_PAYMENT

    df = df[1:]  # drop first two rows
    df.columns = df.iloc[0]  # the first row now contains header names
    df = df[1:]
    df.rename(columns={'Booking Date': 'Datum'},  inplace=True)
    df['Datum'] = pd.to_datetime(df['Datum'],  format='%d.%m.%Y %H:%M')
    df['Datum'] = df['Datum'].dt.strftime('%d.%m.%Y')
    df['Twino_Cashflow-Typ'] = df['Type'] + ' ' + df['Description']
    df['Cashflow-Typ'] = df['Twino_Cashflow-Typ'].map(twino_dict)
    df['Plattform'] = 'Twino'
    df['Währung'] = 'EUR'

    missing_cf_types = check_missing_cf_types(df, 'Twino_Cashflow-Typ')

    df_result = pd.pivot_table(
        df, values='Amount, EUR',
        index=['Plattform', 'Datum', 'Währung'],
        columns=['Cashflow-Typ'],
        aggfunc=sum
    )
    df_result.fillna(0, inplace=True)

    return [df_result, missing_cf_types]
