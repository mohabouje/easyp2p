#  Copyright (c) 2018-2020 Niko Sandschneider

"""
Download and parse Estateguru statement.

"""

from datetime import date
from typing import Optional, Tuple

import pandas as pd
from PyQt5.QtCore import QCoreApplication

from easyp2p.p2p_parser import P2PParser
from easyp2p.p2p_session import P2PSession
from easyp2p.p2p_signals import Signals

_translate = QCoreApplication.translate


class Estateguru:

    """
    Contains methods for downloading/parsing Estateguru account statements.
    """

    def __init__(
            self, date_range: Tuple[date, date],
            statement_without_suffix: str,
            signals: Optional[Signals] = None) -> None:
        """
        Constructor of Estateguru class.

        Args:
            date_range: Date range (start_date, end_date) for which the account
                statements must be generated.
            statement_without_suffix: File name including path but without
                suffix where the account statement should be saved.
            signals: Signals instance for communicating with the calling class.

        """
        self.name = 'Estateguru'
        self.date_range = date_range
        self.statement = statement_without_suffix + '.csv'
        self.signals = signals

    def download_statement(self) -> None:
        """
        Generate and download the Estateguru account statement for given date
        range.

        """
        login_url = 'https://estateguru.co/portal/login/authenticate'
        logout_url = 'https://estateguru.co/portal/logoff'
        statement_url = 'https://estateguru.co/portal/portfolio/account'
        gen_statement_url = (
            'https://estateguru.co/portal/portfolio/ajaxFilterTransactions')

        with P2PSession(self.name, logout_url, self.signals) as sess:
            sess.log_into_page(login_url, 'username', 'password')

            download_url = sess.get_url_from_partial_link(
                statement_url, 'downloadOrderReport.csv', _translate(
                    'P2PPlatform',
                    f'{self.name}: loading account statement page failed!'))
            user_id = download_url.split('&')[1].split('=')[1]

            data = {
                'currentUserId': user_id,
                'currentCurrency': "EUR",
                'userDetails': "",
                'showFutureTransactions': "false",
                'order': "",
                'sort': "",
                'filter_isFilter': "[true]",
                'filterTableId': "dataTableTransaction",
                'filter_dateApproveFilterFrom':
                    f"[{self.date_range[0].strftime('%d.%m.%Y')}]",
                'filter_dateApproveFilterTo':
                    f"[{self.date_range[1].strftime('%d.%m.%Y')}]",
                'filter_loanName': "",
                'controller': "portfolio",
                'format': "null",
                'action': "ajaxFilterTransactions",
                'max': "20",
                'offset': "40"
            }
            sess.generate_account_statement(gen_statement_url, 'post', data)

            sess.download_statement(
                f'https://estateguru.co{download_url}', self.statement, 'get')

    def parse_statement(self, statement: Optional[str] = None) \
            -> Tuple[pd.DataFrame, Tuple[str, ...]]:
        """
        Parser for Estateguru.

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
            self.name, self.date_range, self.statement, skipfooter=1,
            signals=self.signals)

        # Only consider valid cash flows
        parser.df = parser.df[parser.df['Cash Flow Status'] == 'Approved']

        # Define mapping between Estateguru and easyp2p cash flow types and
        # column names
        cashflow_types = {
            # Treat bonus payments as normal interest payments
            'Bonus': parser.INTEREST_PAYMENT,
            'Deposit': parser.IN_OUT_PAYMENT,
            'Withdrawal': parser.IN_OUT_PAYMENT,
            'Indemnity': parser.LATE_FEE_PAYMENT,
            'Principal': parser.REDEMPTION_PAYMENT,
            'Investment(Auto Invest)': parser.INVESTMENT_PAYMENT,
            'Penalty': parser.LATE_FEE_PAYMENT,
            'Interest': parser.INTEREST_PAYMENT}
        rename_columns = {
            'Cash Flow Type': 'EG Cash Flow Type',
            'Confirmation Date': parser.DATE}

        unknown_cf_types = parser.parse(
            '%d/%m/%Y %H:%M', rename_columns, cashflow_types,
            'EG Cash Flow Type', 'Amount', 'Available to invest')

        return parser.df, unknown_cf_types
