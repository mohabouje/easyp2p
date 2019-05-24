# -*- coding: utf-8 -*-
# Copyright 2018-19 Niko Sandschneider

"""
Download and parse Robocash statement.

"""

from datetime import date
from typing import Optional, Tuple

import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

from easyp2p.p2p_parser import P2PParser
from easyp2p.p2p_platform import P2PPlatform
from easyp2p.p2p_webdriver import P2PWebDriver


class Robocash:

    """
    Contains methods for downloading/parsing Robocash account statements.
    """

    def __init__(
            self, date_range: Tuple[date, date],
            statement_without_suffix: str) -> None:
        """
        Constructor of Robocash class.

        Args:
            date_range: Date range (start_date, end_date) for which the account
                statements must be generated.
            statement_without_suffix: File name including path but without
                suffix where the account statement should be saved.

        """
        self.name = 'Robocash'
        self.date_range = date_range
        self.statement = statement_without_suffix + '.xls'

    def download_statement(
            self, driver: P2PWebDriver, credentials: Tuple[str, str]) -> None:
        """
        Generate and download the Robocash account statement.

        Args:
            driver: Instance of P2PWebDriver class.
            credentials: Tuple (username, password) for Robocash.

        Raises:
            RuntimeError: - If the statement button cannot be found
                          - If the download of the statement takes too long

        """
        urls = {
            'login': 'https://robo.cash/de',
            'logout': 'https://robo.cash/de/logout',
            'statement': 'https://robo.cash/de/cabinet/statement',
        }
        xpaths = {
            'login_field': '/html/body/header/div/div[2]/a',
        }

        # TODO: do not rely on text in title for checking successful logout
        with P2PPlatform(
                self.name, driver, urls,
                EC.title_contains('Willkommen')) as robocash:

            robocash.log_into_page(
                'email', 'password', credentials,
                EC.element_to_be_clickable((By.LINK_TEXT, 'Kontoauszug')),
                login_locator=(By.XPATH, xpaths['login_field']))

            robocash.open_account_statement_page((By.ID, 'new_statement'))

            try:
                driver.find_element_by_id('new_statement').click()
            except NoSuchElementException:
                raise RuntimeError(
                    'Generierung des Robocash-Kontoauszugs konnte nicht '
                    'gestartet werden.')

            robocash.generate_statement_direct(
                self.date_range, (By.ID, 'date-after'),
                (By.ID, 'date-before'), '%Y-%m-%d')

            # Robocash does not automatically show download button after
            # statement generation is done. An explicit reload of the page is
            # needed.
            present = False
            wait = 0
            while not present:
                try:
                    driver.get(urls['statement'])
                    driver.wait(EC.element_to_be_clickable(
                        (By.ID, 'download_statement')))
                    present = True
                except TimeoutException:
                    wait += 1
                    if wait > 10:  # Roughly 10*delay seconds
                        raise RuntimeError(
                            'Generierung des {0}-Kontoauszugs hat zu lange '
                            'gedauert!'.format(self.name))

            robocash.download_statement(
                self.statement, (By.ID, 'download_statement'))

    def parse_statement(self, statement: Optional[str] = None) \
            -> Tuple[pd.DataFrame, str]:
        """
        Parser for Robocash.

        Args:
            statement: File name including path of the account
                statement which should be parsed. If None, the file at
                self.statement will be parsed. Default is None.

        Returns:
            Tuple with two elements. The first element is the data frame
            containing the parsed results. The second element is a set
            containing all unknown cash flow types.

        """
        if statement:
            self.statement = statement

        parser = P2PParser(self.name, self.date_range, self.statement)

        # Define mapping between Robocash and easyp2p cashflow types and
        # column names
        cashflow_types = {
            'Darlehenskauf': parser.INVESTMENT_PAYMENT,
            'Die Geldauszahlung': parser.OUTGOING_PAYMENT,
            'Geldeinzahlung': parser.INCOMING_PAYMENT,
            'Kreditrückzahlung': parser.REDEMPTION_PAYMENT,
            # We don't report cash transfers within Robocash:
            'Portfolio auffüllen': parser.IGNORE,
            'Zinsenzahlung': parser.INTEREST_PAYMENT}
        rename_columns = {'Datum und Laufzeit': parser.DATE}

        unknown_cf_types = parser.run(
            '%Y-%m-%d %H:%M:%S', rename_columns, cashflow_types,
            'Operation', 'Betrag', 'Der Saldo des Portfolios')

        return parser.df, unknown_cf_types
