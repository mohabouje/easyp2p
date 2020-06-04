#  Copyright (c) 2018-2020 Niko Sandschneider

"""
Download and parse Iuvo statement.

"""

from bs4 import BeautifulSoup
from PyQt5.QtCore import QCoreApplication
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from easyp2p.p2p_parser import P2PParser
from easyp2p.p2p_webdriver import P2PWebDriver, download_finished
from easyp2p.platforms.base_platform import BasePlatform

_translate = QCoreApplication.translate


class Iuvo(BasePlatform):
    """
    Contains methods for downloading/parsing Iuvo account statements.
    """

    NAME = 'Iuvo'
    SUFFIX = 'xlsx'
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    RENAME_COLUMNS = {'Date': P2PParser.DATE}
    CASH_FLOW_TYPES = {
        'deposit': P2PParser.IN_OUT_PAYMENT,
        'late_fee': P2PParser.LATE_FEE_PAYMENT,
        'payment_interest': P2PParser.INTEREST_PAYMENT,
        'payment_interest_early': P2PParser.INTEREST_PAYMENT,
        'primary_market_auto_invest': P2PParser.INVESTMENT_PAYMENT,
        'payment_principal_buyback': P2PParser.BUYBACK_PAYMENT,
        'payment_principal': P2PParser.REDEMPTION_PAYMENT,
        'payment_principal_early': P2PParser.REDEMPTION_PAYMENT,
    }
    ORIG_CF_COLUMN = 'Transaction Type'
    VALUE_COLUMN = 'Turnover'
    BALANCE_COLUMN = 'Balance'
    HEADER = 3
    SKIP_FOOTER = 3

    def download_statement(  # pylint: disable=arguments-differ
            self, headless: bool) -> None:
        """
        Generate and download the Iuvo account statement for given date range.

        Args:
            headless: If True use ChromeDriver in headless mode, if False not.

        """
        urls = {
            'login': 'https://www.iuvo-group.com/en/login/',
            'statement': 'https://www.iuvo-group.com/en/account-statement/',
        }

        with P2PWebDriver(
                self.NAME, headless, urls,
                EC.element_to_be_clickable((By.ID, 'login')),
                logout_locator=(By.ID, 'p2p_logout'),
                hover_locator=(By.LINK_TEXT, 'User name'),
                signals=self.signals) as iuvo:

            iuvo.log_into_page(
                'login', 'password',
                EC.element_to_be_clickable((By.LINK_TEXT, 'Account Statement')))

            # Click away cookie policy, if present
            iuvo.driver.click_button(
                (By.ID, 'CybotCookiebotDialogBodyButtonAccept'), 'Ignored',
                raise_error=False)

            iuvo.open_account_statement_page((By.ID, 'date_from'))
            soup = BeautifulSoup(iuvo.driver.page_source, 'html.parser')
            try:
                account_id = soup.input["value"]
                p2_var = iuvo.driver.current_url.split(';')[1]
            except (KeyError, IndexError):
                raise RuntimeError(_translate(
                    'P2PPlatform',
                    f'{self.NAME}: loading account statement page was not '
                    'successful!'))

            iuvo.driver.get(
                f'https://tbp2p.iuvo-group.com/p2p-ui/app?p0=export_file;'
                f'{p2_var};;display_as=export;'
                f'export_as=xlsx;sid=rep_account_statement_full_list;sr=1;'
                f'rep_name=AccountStatement;'
                f'investor_account_id={account_id}&'
                f'date_from={self.date_range[0].strftime("%Y-%m-%d")}&'
                f'date_to={self.date_range[1].strftime("%Y-%m-%d")};'
                f'lang=en_US&screen_width=1920&screen_height=780')

            if not download_finished(
                    self.statement, iuvo.driver.download_directory):
                raise RuntimeError(_translate(
                    'P2PPlatform',
                    f'{self.NAME}: download of account statement failed!'))
