# -*- coding: utf-8 -*-
# Copyright 2018-19 Niko Sandschneider

"""
This module contains functions for preparing test files with expected results.

The files will be used by easyp2p_tests to compare the actual to the expected
results.

"""
from datetime import date

from context import *
import easyp2p_tests


def generate_parser_results():
    """
    Generate the expected result files for the unit tests.

    This function generates the expected results files for the parser unit
    tests. It can generate the default, unknown cashflow type, no cashflows
    and unknown currency result files. Since it uses the code which these
    expected results should test, the result files need to be checked manually
    before using them!

    """
    for elem in easyp2p_tests.PLATFORMS:
        # DoFinance has its own date range
        if elem == 'DoFinance':
            date_range = (date(2018, 5, 1), date(2018, 9, 30))
        else:
            date_range = (date(2018, 9, 1), date(2018, 12, 31))
        input_file = easyp2p_tests.INPUT_PREFIX + '{0}_parser.{1}'.format(
            elem.lower(), easyp2p_tests.PLATFORMS[elem])
        output_file = easyp2p_tests.RESULT_PREFIX + '{0}_parser.csv'.format(
            elem.lower())
        parser = getattr(
            getattr(sys.modules[__name__], elem.lower()),
            'parse_statement')
        (df, _) = parser(date_range, input_file)
        df.to_csv(output_file)

    for elem in ['Estateguru', 'Mintos', 'Grupeer', 'DoFinance', 'Twino']:
        #TODO: generate the unknown cf input files
        if elem == 'DoFinance':
            date_range = (date(2018, 5, 1), date(2018, 9, 30))
        else:
            date_range = (date(2018, 9, 1), date(2018, 12, 31))
        input_file = easyp2p_tests.INPUT_PREFIX \
            + '{0}_parser_unknown_cf.{1}'.format(
                elem.lower(), easyp2p_tests.PLATFORMS[elem])
        output_file = easyp2p_tests.RESULT_PREFIX \
            + '{0}_parser_unknown_cf.csv'.format(
                elem.lower())
        parser = getattr(
            getattr(sys.modules[__name__], elem.lower()),
            'parse_statement')
        (df, _) = parser(date_range, input_file)
        df.to_csv(output_file)

    for elem in easyp2p_tests.PLATFORMS:
        input_file = easyp2p_tests.INPUT_PREFIX \
            + '{0}_parser_missing_month.{1}'.format(
                elem.lower(), easyp2p_tests.PLATFORMS[elem])
        output_file = easyp2p_tests.RESULT_PREFIX \
            + '{0}_parser_missing_month.csv'.format(
                elem.lower())
        parser = getattr(
            getattr(sys.modules[__name__], elem.lower()),
            'parse_statement')

        # DoFinance has its own date range
        if elem == 'DoFinance':
            date_range = (date(2018, 5, 1), date(2018, 9, 30))
        else:
            date_range = (date(2018, 8, 1), date(2018, 12, 31))
        (df, _) = parser(date_range, input_file)
        df.to_csv(output_file)

    for elem in easyp2p_tests.PLATFORMS:
        input_file = easyp2p_tests.INPUT_PREFIX \
            + '{0}_parser_no_cfs.{1}'.format(
                elem.lower(), easyp2p_tests.PLATFORMS[elem])
        output_file = easyp2p_tests.RESULT_PREFIX \
            + '{0}_parser_no_cfs.csv'.format(
                elem.lower())
        parser = getattr(
            getattr(sys.modules[__name__], elem.lower()),
            'parse_statement')
        (df, _) = parser((date(2016, 9, 1), date(2016, 12, 31)), input_file)
        df.to_csv(output_file)

    for elem in ['Grupeer']:
        input_file = easyp2p_tests.INPUT_PREFIX \
            + '{0}_parser_unknown_currency.{1}'.format(
                elem.lower(), easyp2p_tests.PLATFORMS[elem])
        output_file = easyp2p_tests.RESULT_PREFIX \
            + '{0}_parser_unknown_currency.csv'.format(
                elem.lower())
        parser = getattr(
            getattr(sys.modules[__name__], elem.lower()),
            'parse_statement')
        (df, _) = parser(date_range, input_file)
        df.to_csv(output_file)

if __name__ == '__main__':
    generate_parser_results()