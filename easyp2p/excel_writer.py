# -*- coding: utf-8 -*-
#  Copyright (c) 2018-2020 Niko Sandschneider

"""
Module for writing parsed account statements of P2P platforms to Excel.

The combined parsed results of all selected P2P platforms will be written to
an Excel file with three worksheets: daily results, monthly results and total
results for the whole date range.

"""
import calendar
from datetime import date, timedelta
import logging
from typing import Callable, Dict, List, Optional, Sequence, Tuple

import pandas as pd
from PyQt5.QtCore import QCoreApplication

from easyp2p.p2p_signals import Signals
from easyp2p.p2p_parser import P2PParser

_translate = QCoreApplication.translate
logger = logging.getLogger('easyp2p.excel_writer')

DAILY_RESULTS = _translate('excel_writer', 'Daily results')
MONTHLY_RESULTS = _translate('excel_writer', 'Monthly results')
TOTAL_RESULTS = _translate('excel_writer', 'Total results')

# Signals for communicating with the GUI
signals = Signals()


@signals.update_progress
def write_results(
        df_result: pd.DataFrame, output_file: str,
        date_range: Tuple[date, date]) -> bool:
    """
    Function for writing daily, monthly and total investment results to Excel.

    Args:
        df_result: DataFrame containing parsed account statements for all
            selected P2P platforms.
        output_file: File name including path where to save the Excel file.
        date_range: Date range (start_date, end_date) for which the account
            statement was generated.

    Returns:
        True on success, False on failure.

    Raises:
        RuntimeError: If date, platform or currency column are missing
            in df_result.

    """
    # Check if there were any results
    if df_result.empty:
        logger.info('df_result is empty.')
        return False

    # Make a copy to prevent changing the original DataFrame
    df_result = df_result.copy()
    df_result.reset_index(inplace=True)

    # Make sure that all index columns are present
    for column in [P2PParser.PLATFORM, P2PParser.CURRENCY, P2PParser.DATE]:
        if column not in df_result.columns:
            raise RuntimeError(
                _translate(
                    'excel_writer', 'Writing results to Excel was not '
                    f'successful! Column {column} is missing!'))

    # Format date column and add month column to DataFrame
    df_result[P2PParser.DATE] = pd.to_datetime(
        df_result[P2PParser.DATE], format='%Y-%m-%d')
    df_result[P2PParser.MONTH] = pd.to_datetime(
        df_result[P2PParser.DATE], format='%d.%m.%Y').dt.to_period('M')

    # Get daily, monthly and total results
    df_daily = _get_daily_results(df_result)
    df_monthly = _get_monthly_results(df_result, date_range)
    df_total = _get_total_results(df_monthly)

    # Write all three DataFrames to Excel
    with pd.ExcelWriter(
            output_file, datetime_format='DD.MM.YYYY',
            engine='xlsxwriter') as writer:
        _write_worksheet(writer, DAILY_RESULTS, df_daily)
        _write_worksheet(writer, MONTHLY_RESULTS, df_monthly)
        _write_worksheet(writer, TOTAL_RESULTS, df_total)

    return True


def _get_daily_results(df_result: pd.DataFrame) -> pd.DataFrame:
    """
    Get daily results from DataFrame.

    Args:
        df_result: DataFrame containing parsed account statements for all
            selected P2P platforms.

    Returns:
        DataFrame with the daily results.

    """
    df = df_result.copy()
    df.drop(columns=P2PParser.MONTH, inplace=True)
    df.set_index(
        [P2PParser.PLATFORM, P2PParser.CURRENCY, P2PParser.DATE],
        inplace=True)
    df.sort_index(inplace=True)

    return df


def _get_monthly_results(
        df_result: pd.DataFrame, date_range: Tuple[date, date]) -> pd.DataFrame:
    """
    Get monthly results from DataFrame.

    Args:
        df_result: DataFrame containing parsed account statements for all
            selected P2P platforms.
        date_range: Date range for displaying monthly results.

    Returns:
        DataFrame with the monthly results.

    """
    # Define index and columns to aggregate for pivot table
    index = [P2PParser.PLATFORM, P2PParser.CURRENCY, P2PParser.MONTH]
    pivot_columns = [
        column for column in P2PParser.TARGET_COLUMNS
        if column in df_result.columns]
    df = df_result.pivot_table(
        values=pivot_columns, index=index, aggfunc=_get_aggfunc(pivot_columns))
    df = _add_months_without_cashflows(df, date_range)
    return df


def _get_total_results(df_monthly: pd.DataFrame) -> pd.DataFrame:
    """
    Get total results from DataFrame.

    Args:
        df_monthly: DataFrame containing monthly results.

    Returns:
        DataFrame with the total results.

    """
    # Define index and columns to aggregate for pivot table
    index = [P2PParser.PLATFORM, P2PParser.CURRENCY]
    pivot_columns = [
        column for column in P2PParser.TARGET_COLUMNS
        if column in df_monthly.columns]
    df_pivot = df_monthly.pivot_table(
        values=pivot_columns, index=index, aggfunc=_get_aggfunc(pivot_columns),
        dropna=False)

    # Create the total row per currency
    df_total = df_pivot.reset_index().set_index(P2PParser.CURRENCY)
    df_total = df_total.groupby(P2PParser.CURRENCY).sum()
    df_total[P2PParser.PLATFORM] = 'Total'
    df_total = df_total.reset_index().set_index(
        [P2PParser.PLATFORM, P2PParser.CURRENCY])
    df = df_pivot.append(df_total, sort=True)
    df.dropna(how='all', inplace=True)

    return df


def _get_aggfunc(columns: Sequence[str]) -> Dict[str, Callable]:
    """
    Returns the aggregation function for building the pivot tables.

    All columns except the balance columns will be summed up. For the start
    (end) balance columns the first (last) entry per aggregation index will be
    used.

    Returns:
        Dictionary where columns are the keys and the aggregation function are
        the values.

    """
    aggfunc = dict()
    for col in columns:
        if col == P2PParser.START_BALANCE_NAME:
            aggfunc[col] = lambda x: x.iloc[0]
        elif col == P2PParser.END_BALANCE_NAME:
            aggfunc[col] = lambda x: x.iloc[-1]
        else:
            # Only sum up columns with at least one non-NaN value. Otherwise
            # NaN columns will be replaced by zeros.
            aggfunc[col] = lambda x: x.sum(min_count=1)
    return aggfunc


def _add_months_without_cashflows(
        df: pd.DataFrame, date_range: Tuple[date, date]) -> pd.DataFrame:
    """
    Add a zero line for all months in date_range without cash flows.

    Args:
        df: DataFrame which should be checked for missing months.
        date_range: Date range.

    Returns:
        Input DataFrame with zero lines appended for each month without
        cash flows.

    """
    months = get_list_of_months(date_range)

    # For each platform/currency combination we expect one row per month
    # in date_range
    expected_rows = sorted(list(set(
        (index[0], index[1], i) for index in df.index for i in range(
            len(months)))))
    for platform, currency, i in expected_rows:
        month = pd.Period(freq='M', year=months[i].year, month=months[i].month)
        if (platform, currency, month) not in df.index:
            # Only fill columns with non-N/A values
            fill_columns = df.loc[platform].dropna(axis=1).columns
            df.loc[(platform, currency, month), fill_columns] = 0.

            # Zero is not necessarily correct for the balance columns
            if {P2PParser.START_BALANCE_NAME,
                    P2PParser.END_BALANCE_NAME}.issubset(df.columns):
                if i > 0:
                    previous_month = pd.Period(
                        freq='M', year=months[i - 1].year,
                        month=months[i - 1].month)
                    balance = _get_balance_for_months_without_cashflows(
                        df, platform, currency, previous_month)
                else:
                    balance = _get_balance_for_months_without_cashflows(
                        df, platform, currency)
                df.loc[
                    (platform, currency, month),
                    P2PParser.START_BALANCE_NAME] = balance
                df.loc[
                    (platform, currency, month),
                    P2PParser.END_BALANCE_NAME] = balance
    df.sort_index(inplace=True)
    return df


def _get_balance_for_months_without_cashflows(
        df: pd.DataFrame, platform: str, currency: str,
        previous_month: Optional[pd.Period] = None):

    if previous_month:
        # If month is not the first month look up the correct value in
        # previous month's row
        balance = (
            df.loc[
                (platform, currency, previous_month),
                P2PParser.END_BALANCE_NAME])
    else:
        # If month is the first month look up the correct value in the
        # first existing month's row. If no month has cash flows assume
        # that balance=0.
        next_months = [index[2] for index in df.index]
        if next_months:
            balance = (
                df.loc[
                    (platform, currency, next_months[0]),
                    P2PParser.START_BALANCE_NAME])
        else:
            balance = 0
    return balance


def get_list_of_months(date_range: Tuple[date, date]) -> List[date]:
    """
    Get list of all months in date_range.

    Args:
        date_range: Date range.

    Returns:
        List of all months in date_range.

    """
    months = []
    current_date = date_range[0]
    while current_date < date_range[1]:
        days_in_month = calendar.monthrange(
            current_date.year, current_date.month)[1]
        months.append(current_date)
        current_date += timedelta(days=days_in_month)

    return months


def _write_worksheet(
        writer: pd.ExcelWriter, worksheet_name: str, df: pd.DataFrame) -> None:
    """
    Write DataFrame to Excel worksheet and format columns.

    For each column in the worksheet the width is set to the maximum length
    * 1,2 of all entries in the column. For all non-index columns the_format
    is set to money_format.

    Args:
        writer: Handle of pandas ExcelWriter.
        worksheet_name: Name of the worksheet where DataFrame should be
            saved.
        df: DataFrame containing the data to be written to the worksheet.

    """
    # Rounds results to 2 digits, sort columns and fill in missing values
    df = df.round(2)
    df = df[[
        column for column in P2PParser.TARGET_COLUMNS
        if column in df.columns]]
    df.fillna('N/A', inplace=True)

    # Define format for currency columns
    workbook = writer.book
    money_format = workbook.add_format({'num_format': '#,##0.00'})

    df.to_excel(writer, worksheet_name)

    # Format cells and set column widths
    worksheet = writer.sheets[worksheet_name]
    index_length = len(df.index.names)
    df = df.reset_index()
    for index, col in enumerate(df.columns):
        # Get length of header and longest data entry
        header_length = len(col)
        data_length = df[col].map(lambda x: len(str(x))).max()
        if index < index_length:
            worksheet.set_column(
                index, index, max(header_length, data_length) * 1.2)
        else:
            worksheet.set_column(
                index, index, max(header_length, data_length) * 1.2,
                money_format)
