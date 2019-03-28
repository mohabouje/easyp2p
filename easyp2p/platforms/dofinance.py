# -*- coding: utf-8 -*-
# Copyright 2018-19 Niko Sandschneider

"""
Download and parse DoFinance statement.

.. moduleauthor:: Niko Sandschneider <nsandschn@gmx.de>

"""

from datetime import date
import os
from typing import Tuple

import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from easyp2p.p2p_parser import P2PParser
from easyp2p.p2p_platform import P2PPlatform


class DoFinance:

    def __init__(self, date_range: Tuple[date, date]) -> None:
        """
        Constructor of DoFinance class.

        Args:
            date_range: date range (start_date, end_date) for which the account
                statements must be generated

        """
        self.name = 'DoFinance'
        self.date_range = date_range

    def download_statement(self, credentials: Tuple[str, str]) -> None:
        """
        Generate and download the DoFinance account statement.

        Args:
            credentials: (username, password) for DoFinance

        """
        urls = {
            'login': 'https://www.dofinance.eu/de/users/login',
            'logout': 'https://www.dofinance.eu/de/users/logout',
            'statement': 'https://www.dofinance.eu/de/users/statement'}
        default_file_name = 'Statement_{0} 00_00_00-{1} 23_59_59*.xlsx'.format(
            self.date_range[0].strftime('%Y-%m-%d'),
            self.date_range[1].strftime('%Y-%m-%d'))

        with P2PPlatform(
                'DoFinance', urls,
                EC.title_contains('Kreditvergabe Plattform')) as dofinance:

            self.statement_file_name = dofinance.set_statement_file_name(
                self.date_range, 'xlsx')

            dofinance.log_into_page(
                'email', 'password', credentials,
                EC.element_to_be_clickable((By.LINK_TEXT, 'TRANSAKTIONEN')))

            dofinance.open_account_statement_page(
                'Transaktionen', (By.ID, 'date-from'))

            dofinance.generate_statement_direct(
                self.date_range, (By.ID, 'date-from'), (By.ID, 'date-to'),
                '%d.%m.%Y',
                wait_until=EC.element_to_be_clickable((By.NAME, 'xls')))

            dofinance.download_statement(
                default_file_name, self.statement_file_name, (By.NAME, 'xls'))


    def parse_statement(self, statement_file_name: str = None) \
            -> Tuple[pd.DataFrame, str]:
        """
        Parser for DoFinance.

        Keyword Args:
            statement_file_name: File name including path of the account
                statement which should be parsed

        Returns:
            Tuple with two elements. The first
            element is the data frame containing the parsed results. The second
            element is a set containing all unknown cash flow types.

        """
        if statement_file_name is not None:
            self.statement_file_name = statement_file_name
        elif not os.path.exists(self.statement_file_name):
            raise RuntimeError(
                'Kontoauszugsdatei {0} konnte nicht gefunden werden!'
                .format(self.statement_file_name))

        parser = P2PParser(self.name, self.date_range, self.statement_file_name)

        # Create a DataFrame with zero entries if there were no cashflows
        if parser.df.empty:
            parser.parse_statement()
            return (parser.df, '')

        # Drop the last two rows which only contain a summary
        parser.df = parser.df[:-2]

        # Define mapping between DoFinance and easyp2p cashflow types and
        # column names
        cashflow_types = {
            'Abhebungen': parser.OUTGOING_PAYMENT,
            'Gewinn': parser.INTEREST_PAYMENT}

        for interest_rate in ['5%', '7%', '9%', '12%']:
            cashflow_types[
                'Rückzahlung\nRate: {0} Typ: automatisch'
                .format(interest_rate)] = parser.REDEMPTION_PAYMENT
            cashflow_types[
                'Anlage\nRate: {0} Typ: automatisch'.format(interest_rate)] \
                = parser.INVESTMENT_PAYMENT

        rename_columns = {'Bearbeitungsdatum': parser.DATE}

        unknown_cf_types = parser.parse_statement(
            '%d.%m.%Y', rename_columns, cashflow_types, 'Art der Transaktion',
            'Betrag, €')

        return (parser.df, unknown_cf_types)
