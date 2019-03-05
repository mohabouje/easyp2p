# -*- coding: utf-8 -*-
# Copyright 2018-19 Niko Sandschneider

"""
Download and parse Twino statement.

.. moduleauthor:: Niko Sandschneider <nsandschn@gmx.de>

"""

from datetime import date
from typing import Tuple

import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from p2p_parser import P2PParser
from p2p_platform import P2PPlatform


def download_statement(
        date_range: Tuple[date, date],
        credentials: Tuple[str, str]) -> None:
    """
    Generate and download the Twino account statement for given date range.

    Args:
        date_range (tuple(date, date)): date range
            (start_date, end_date) for which the account statements must
            be generated.
        credentials (tuple[str, str]): (username, password) for Twino

    """
    urls = {
        'login': 'https://www.twino.eu/de/',
        'statement': ('https://www.twino.eu/de/profile/investor/'
                      'my-investments/account-transactions')}
    xpaths = {
        'end_date': '//*[@date-picker="filterData.processingDateTo"]',
        'login_btn': ('/html/body/div[1]/div[2]/div[1]/header[1]/div/nav/div/'
                      'div[1]/button'),
        'logout_btn': '//a[@href="/logout"]',
        'start_date': '//*[@date-picker="filterData.processingDateFrom"]',
        'statement': ('//a[@href="/de/profile/investor/my-investments/'
                      'individual-investments"]')}

    with P2PPlatform(
            'Twino', urls,
            EC.element_to_be_clickable((By.XPATH, xpaths['login_btn'])),
            logout_locator=(By.XPATH, xpaths['logout_btn'])) as twino:

        twino.log_into_page(
            'email', 'login-password', credentials,
            EC.element_to_be_clickable((By.XPATH, xpaths['statement'])),
            login_locator=(By.XPATH, xpaths['login_btn']))

        twino.open_account_statement_page(
            'TWINO', (By.XPATH, xpaths['start_date']))

        twino.generate_statement_direct(
            date_range, (By.XPATH, xpaths['start_date']),
            (By.XPATH, xpaths['end_date']), '%d.%m.%Y',
            wait_until=EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '.accStatement__pdf')))

        twino.download_statement(
            'account_statement_*.xlsx',
            (By.CSS_SELECTOR, '.accStatement__pdf'))


def parse_statement(
        date_range: Tuple[date, date],
        input_file: str = 'p2p_downloads/twino_statement.xlsx') \
        -> Tuple[pd.DataFrame, str]:
    """
    Parser for Twino.

    Args:
        date_range (tuple(date, date)): date range
            (start_date, end_date) for which the investment results must be
            shown.

    Keyword Args:
        input_file (str): file name including path of the account statement
            downloaded from the Twino web site

    Returns:
        tuple(pandas.DataFrame, set(str)): tuple with two elements. The first
        element is the data frame containing the parsed results. The second
        element is a set containing all unknown cash flow types.

    """
    parser = P2PParser('Twino', date_range, input_file)

    # Format the header of the table
    parser.df = parser.df[1:]  # The first row only contains a generic header
    new_header = parser.df.iloc[0] # Get the new first row as header
    parser.df = parser.df[1:] # Remove the first row
    parser.df.columns = new_header # Set the new header

    # Create a DataFrame with zero entries if there were no cashflows
    if parser.df.empty:
        parser.parse_statement()
        return (parser.df, '')

    # Create a new column for identifying cashflow types
    try:
        parser.df['Twino_Cashflow-Typ'] = parser.df['Type'] + ' ' \
            + parser.df['Description']
    except KeyError:
        raise RuntimeError(
            'Twino: Cashflowspalte nicht im Kontoauszug vorhanden!')

    # Define mapping between Twino and easyP2P cashflow types and column names
    cashflow_types = {
        'BUYBACK INTEREST': parser.BUYBACK_INTEREST_PAYMENT,
        'BUYBACK PRINCIPAL': parser.BUYBACK_PAYMENT,
        'BUY_SHARES PRINCIPAL': parser.INVESTMENT_PAYMENT,
        'EXTENSION INTEREST': parser.INTEREST_PAYMENT,
        'REPAYMENT INTEREST': parser.INTEREST_PAYMENT,
        'REPAYMENT PRINCIPAL': parser.REDEMPTION_PAYMENT,
        'REPURCHASE INTEREST': parser.BUYBACK_INTEREST_PAYMENT,
        'REPURCHASE PRINCIPAL': parser.BUYBACK_PAYMENT,
        'SCHEDULE INTEREST': parser.INTEREST_PAYMENT
        }
    rename_columns = {'Processing Date': parser.DATE}

    unknown_cf_types = parser.parse_statement(
        '%d.%m.%Y %H:%M', rename_columns, cashflow_types, 'Twino_Cashflow-Typ',
        'Amount, EUR')

    return (parser.df, unknown_cf_types)