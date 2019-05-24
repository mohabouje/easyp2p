# Copyright 2018-19 Niko Sandschneider

"""
Download and parse Iuvo statement.

"""

from datetime import date
from typing import Optional, Tuple

import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from easyp2p.p2p_parser import P2PParser
from easyp2p.p2p_platform import P2PPlatform
from easyp2p.p2p_webdriver import (
    P2PWebDriver, one_of_many_expected_conditions_true)


class Iuvo:
    """
    Contains methods for downloading/parsing Iuvo account statements.
    """

    def __init__(
            self, date_range: Tuple[date, date],
            statement_without_suffix: str) -> None:
        """
        Constructor of Iuvo class.

        Args:
            date_range: Date range (start_date, end_date) for which the account
                statements must be generated.
            statement_without_suffix: File name including path but without
                suffix where the account statement should be saved.

        """
        self.name = 'Iuvo'
        self.date_range = date_range
        self.statement = statement_without_suffix + '.xlsx'

    def download_statement(
            self, driver: P2PWebDriver, credentials: Tuple[str, str]) -> None:
        """
        Generate and download the Iuvo account statement for given date range.

        Args:
            driver: Instance of P2PWebDriver class.
            credentials: Tuple (username, password) for Iuvo.

        """
        urls = {
            'login': 'https://www.iuvo-group.com/de/login/',
            'statement': 'https://www.iuvo-group.com/de/account-statement/',
        }
        xpaths = {
            'statement_check': (
                '/html/body/div[5]/main/div/div/div/div[6]/div/div/div'
                '/strong[3]'),
        }

        with P2PPlatform(
                self.name, driver, urls,
                EC.element_to_be_clickable((By.ID, 'einloggen')),
                logout_locator=(By.ID, 'p2p_logout'),
                hover_locator=(By.LINK_TEXT, 'User name')) as iuvo:

            iuvo.log_into_page(
                'login', 'password', credentials,
                EC.element_to_be_clickable((By.LINK_TEXT, 'Kontoauszug')))

            # Click away cookie policy, if present
            try:
                driver.find_element_by_id(
                    'CybotCookiebotDialogBodyButtonAccept').click()
            except NoSuchElementException:
                pass

            iuvo.open_account_statement_page((By.ID, 'date_from'))

            check_txt = '{0} - {1}'.format(
                self.date_range[0].strftime('%Y-%m-%d'),
                self.date_range[1].strftime('%Y-%m-%d'))

            # Define conditions if account statement generation is successful:
            # The first condition will be true if there were cashflows in
            # date_range, the second condition will be true of there were none
            conditions = [
                EC.text_to_be_present_in_element(
                    (By.XPATH, xpaths['statement_check']), check_txt),
                EC.text_to_be_present_in_element(
                    (By.CLASS_NAME, 'text-center'), 'Keine passenden Daten!')]

            iuvo.generate_statement_direct(
                (self.date_range[0], self.date_range[1]), (By.ID, 'date_from'),
                (By.ID, 'date_to'), '%Y-%m-%d',
                wait_until=one_of_many_expected_conditions_true(conditions),
                submit_btn_locator=(By.ID, 'account_statement_filters_btn'))

            try:
                no_cashflows = bool(
                    iuvo.driver.find_element_by_class_name(
                        'text-center').text == 'Keine passenden Daten!')
            except NoSuchElementException:
                no_cashflows = False

            # If there were no cashflows write an empty DataFrame to the file
            if no_cashflows:
                df = pd.DataFrame()
                df.to_excel(self.statement)
            else:
                iuvo.download_statement(
                    self.statement,
                    (By.CLASS_NAME, 'p2p-download-full-list'))

    def parse_statement(self, statement: Optional[str] = None) \
            -> Tuple[pd.DataFrame, str]:
        """
        Parser for Iuvo.

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

        parser = P2PParser(
            self.name, self.date_range, self.statement, header=3, skipfooter=3)

        # Define mapping between Iuvo and easyp2p cashflow types and column
        # names
        cashflow_types = {
            'late_fee': parser.LATE_FEE_PAYMENT,
            'payment_interest': parser.INTEREST_PAYMENT,
            'payment_interest_early': parser.INTEREST_PAYMENT,
            'primary_market_auto_invest': parser.INVESTMENT_PAYMENT,
            'payment_principal_buyback': parser.BUYBACK_PAYMENT,
            'payment_principal': parser.REDEMPTION_PAYMENT,
            'payment_principal_early': parser.REDEMPTION_PAYMENT}
        rename_columns = {'Date': parser.DATE}

        unknown_cf_types = parser.run(
            '%Y-%m-%d %H:%M:%S', rename_columns, cashflow_types,
            'Transaction Type', 'Turnover', 'Balance')

        return parser.df, unknown_cf_types
