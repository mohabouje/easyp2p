# -*- coding: utf-8 -*-
# Copyright 2018-19 Niko Sandschneider

"""Module containing all GUI tests for easyp2p."""

from datetime import date
import os
import sys
import unittest

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QLineEdit, QMessageBox
from PyQt5.QtTest import QTest

import easyp2p.p2p_helper as p2p_helper
from easyp2p.ui.main_window import MainWindow
from easyp2p.ui.progress_window import ProgressWindow

PLATFORMS = {
    'Bondora': 'csv',
    'DoFinance': 'xlsx',
    'Estateguru': 'csv',
    'Grupeer': 'xlsx',
    'Iuvo': 'xlsx',
    'Mintos': 'xlsx',
    'PeerBerry': 'csv',
    'Robocash': 'xls',
    'Swaper': 'xlsx',
    'Twino': 'xlsx'}

app = QApplication(sys.argv)


class MainWindowTests(unittest.TestCase):

    """Test the main window of easyp2p."""

    def setUp(self) -> None:
        """Create the GUI."""
        self.form = MainWindow()
        self.message_box_open = False
        self.progress_window_open = False

    def set_test_dates(
            self, start_month: str = 'Sep', start_year: str = '2018',
            end_month: str = 'Jan', end_year: str = '2019') -> None:
        """
        Set start and end dates in the GUI.

        Keyword Args:
            start_month: Start month
            start_year: Start year
            end_month: End month
            end_year: End year

        """
        self.form.combo_box_start_month.setCurrentIndex(
            self.form.combo_box_start_month.findText(start_month))
        self.form.combo_box_start_year.setCurrentIndex(
            self.form.combo_box_start_year.findText(start_year))
        self.form.combo_box_end_month.setCurrentIndex(
            self.form.combo_box_end_month.findText(end_month))
        self.form.combo_box_end_year.setCurrentIndex(
            self.form.combo_box_end_year.findText(end_year))

    def test_defaults(self) -> None:
        """Test GUI in default state."""

        # All checkboxes are unchecked in default state
        self.assertFalse(self.form.check_box_bondora.isChecked())
        self.assertFalse(self.form.check_box_dofinance.isChecked())
        self.assertFalse(self.form.check_box_estateguru.isChecked())
        self.assertFalse(self.form.check_box_grupeer.isChecked())
        self.assertFalse(self.form.check_box_iuvo.isChecked())
        self.assertFalse(self.form.check_box_mintos.isChecked())
        self.assertFalse(self.form.check_box_peerberry.isChecked())
        self.assertFalse(self.form.check_box_robocash.isChecked())
        self.assertFalse(self.form.check_box_select_all.isChecked())
        self.assertFalse(self.form.check_box_swaper.isChecked())
        self.assertFalse(self.form.check_box_twino.isChecked())

        # Check if output file name is set correctly
        date_range = self.form.get_date_range()
        self.assertTrue(self.form.line_edit_output_file.text() == os.path.join(
            os.getcwd(), 'P2P_Ergebnisse_{0}-{1}.xlsx'.format(
                date_range[0].strftime('%d%m%Y'),
                date_range[1].strftime('%d%m%Y'))))

        # Check if combo boxes are set correctly
        start_month = int(p2p_helper.short_month_to_nbr(
            str(self.form.combo_box_start_month.currentText())))
        start_year = self.form.combo_box_start_year.currentText()
        end_month = int(p2p_helper.short_month_to_nbr(
            str(self.form.combo_box_end_month.currentText())))
        end_year = self.form.combo_box_end_year.currentText()
        if date.today().month > 1:
            self.assertEqual(date.today().month - 1, start_month)
            self.assertEqual(str(date.today().year), start_year)
            self.assertEqual(date.today().month - 1, end_month)
            self.assertEqual(str(date.today().year), end_year)
        else:
            self.assertEqual(12, start_month)
            self.assertEqual(str(date.today().year - 1), start_year)
            self.assertEqual(12, end_month)
            self.assertEqual(str(date.today().year -1), end_year)

    def test_select_all_platforms(self) -> None:
        """Test the Select All Platforms checkbox."""
        # Toggle the 'Select all platforms' checkbox
        self.form.check_box_select_all.setChecked(True)

        # Test that all platform check boxes are checked
        self.assertTrue(self.form.check_box_bondora.isChecked())
        self.assertTrue(self.form.check_box_dofinance.isChecked())
        self.assertTrue(self.form.check_box_estateguru.isChecked())
        self.assertTrue(self.form.check_box_grupeer.isChecked())
        self.assertTrue(self.form.check_box_iuvo.isChecked())
        self.assertTrue(self.form.check_box_mintos.isChecked())
        self.assertTrue(self.form.check_box_peerberry.isChecked())
        self.assertTrue(self.form.check_box_robocash.isChecked())
        self.assertTrue(self.form.check_box_select_all.isChecked())
        self.assertTrue(self.form.check_box_swaper.isChecked())
        self.assertTrue(self.form.check_box_twino.isChecked())

    def test_select_all_platforms_twice(self) -> None:
        """Test the Select All Platforms checkbox."""
        # Toggle the 'Select all platforms' checkbox
        self.form.check_box_select_all.setChecked(True)

        # Untoggle the 'Select all platforms' checkbox again
        self.form.check_box_select_all.setChecked(False)

        # Test that all platform check boxes are unchecked again
        self.assertFalse(self.form.check_box_bondora.isChecked())
        self.assertFalse(self.form.check_box_dofinance.isChecked())
        self.assertFalse(self.form.check_box_estateguru.isChecked())
        self.assertFalse(self.form.check_box_grupeer.isChecked())
        self.assertFalse(self.form.check_box_iuvo.isChecked())
        self.assertFalse(self.form.check_box_mintos.isChecked())
        self.assertFalse(self.form.check_box_peerberry.isChecked())
        self.assertFalse(self.form.check_box_robocash.isChecked())
        self.assertFalse(self.form.check_box_select_all.isChecked())
        self.assertFalse(self.form.check_box_swaper.isChecked())
        self.assertFalse(self.form.check_box_twino.isChecked())

    def test_no_platform_selected(self) -> None:
        """Test clicking start without any selected platform."""
        # Push the start button without selecting any platform first
        QTimer.singleShot(500, self.is_message_box_open)
        self.form.push_button_start.click()

        # Check that a warning message pops up
        self.assertTrue(self.message_box_open)

        # Check that the progress window did not open
        self.assertFalse(self.is_progress_window_open())

    def test_output_file_on_date_change(self) -> None:
        """Test output file name after a date change."""
        old_output_file = self.form.line_edit_output_file.text()

        # Change start and/or end date
        self.set_test_dates('Feb', '2017', 'Sep', '2017')
        self.form.on_combo_box_start_month_activated()

        new_output_file = self.form.line_edit_output_file.text()
        self.assertNotEqual(new_output_file, old_output_file)
        self.assertEqual(new_output_file, os.path.join(
            os.getcwd(), 'P2P_Ergebnisse_01022017-30092017.xlsx'))

    def test_output_file_on_date_change_after_user_change(self) -> None:
        """Test output file after date change if user already changed file."""
        QLineEdit.setText(self.form.line_edit_output_file, 'Test.xlsx')
        self.form.output_file_changed = True

        # Change start and/or end date
        self.set_test_dates('Feb', '2017', 'Sep', '2017')
        self.form.on_combo_box_start_month_activated()

        # Check that the output file name was not changed
        self.assertEqual(self.form.line_edit_output_file.text(), 'Test.xlsx')

    def test_end_date_before_start_date(self) -> None:
        """Test clicking start with end date set before start date."""
        self.set_test_dates('Feb', '2017', 'Sep', '2016')

        # Push the start button
        QTimer.singleShot(500, self.is_message_box_open)
        self.form.push_button_start.click()

        # Check that a warning message pops up
        self.assertTrue(self.message_box_open)

        # Check that the progress window did not open
        self.assertFalse(self.is_progress_window_open())

    def is_message_box_open(self) -> bool:
        """Helper method to determine if a QMessageBox is open."""
        all_top_level_widgets = QApplication.topLevelWidgets()
        for widget in all_top_level_widgets:
            if isinstance(widget, QMessageBox):
                QTest.keyClick(widget, Qt.Key_Enter)
                self.message_box_open = True
                return True
        self.message_box_open = False
        return False

    def is_progress_window_open(self) -> bool:
        """Helper method to determine if a ProgressWindow is open."""
        all_top_level_widgets = QApplication.topLevelWidgets()
        for widget in all_top_level_widgets:
            if isinstance(widget, ProgressWindow):
                self.progress_window_open = True
                return True
        self.progress_window_open = False
        return False


class ProgressWindowTests(unittest.TestCase):

    """Test the progress window of easyp2p."""

    def setUp(self):
        """Initialize ProgressWindow."""
        self.form = ProgressWindow()

    def test_defaults(self):
        """Test default behaviour of ProgressWindow."""
        self.assertEqual(self.form.progressBar.value(), 0)
        self.assertEqual(self.form.progressText.isReadOnly(), True)
        self.assertEqual(self.form.progressText.toPlainText(), '')
        self.assertEqual(self.form.pushButton_ok.isEnabled(), False)
        self.assertEqual(self.form.pushButton_abort.isEnabled(), True)


if __name__ == "__main__":
    unittest.main()
