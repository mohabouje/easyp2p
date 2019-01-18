# -*- coding: utf-8 -*-
# Copyright 2018-19 Niko Sandschneider

"""Module implementing MainWindow, the main window of easyP2P."""

import calendar
from datetime import date
import os
from typing import AbstractSet, Mapping, Tuple

from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QLineEdit, QCheckBox
from PyQt5.QtWidgets import QMessageBox
from xlrd.biffh import XLRDError

import p2p_parser
import p2p_results
import p2p_webdriver as wd
from ui.credentials_window import get_credentials
from ui.progress_window import ProgressWindow
from .Ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    """This class defines the main window of easyP2P."""

    def __init__(self, parent=None):
        """
        Constructor.

        Keyword Args:
        parent (QWidget): reference to the parent widget

        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.progress_window = None
        self.worker = None
        self.platforms = set([])
        self.credentials = dict()
        if date.today().month > 1:
            self.start_month = date.today().month - 1
            self.start_year = date.today().year
        else:
            self.start_month = 12
            self.start_year = date.today().year - 1
        self.comboBox_start_month.setCurrentIndex(
            self.comboBox_start_month.findText(
                wd.nbr_to_short_month(str(self.start_month))))
        self.comboBox_start_year.setCurrentIndex(
            self.comboBox_start_year.findText(str(self.start_year)))
        self.end_month = self.start_month
        self.comboBox_end_month.setCurrentIndex(
            self.comboBox_end_month.findText(
                wd.nbr_to_short_month(str(self.end_month))))
        self.end_year = self.start_year
        self.comboBox_end_year.setCurrentIndex(
            self.comboBox_end_year.findText(str(self.end_year)))
        self.set_start_date()
        self.set_end_date()
        self.output_file = os.getcwd() + '/P2P_Ergebnisse_{0}-{1}.xlsx'.format(
            self.start_date.strftime('%d.%m.%Y'),
            self.end_date.strftime('%d.%m.%Y'))
        self.on_lineEdit_output_file_textChanged(self.output_file)

    def set_start_date(self):
        """Helper method to set start date to first day of selected month."""
        self.start_date = date(self.start_year, self.start_month, 1)

    def set_end_date(self):
        """Helper method to set end date to last day of selected month."""
        end_of_month = calendar.monthrange(self.end_year, self.end_month)[1]
        self.end_date = date(self.end_year, self.end_month, end_of_month)

    @pyqtSlot(bool)
    def on_checkBox_bondora_toggled(self, checked):
        """
        Add/remove Bondora to list of platforms.

        Args:
            checked (bool): if True add Bondora, if False remove Bondora

        """
        if checked:
            self.platforms.add('Bondora')
        else:
            self.platforms.remove('Bondora')

    @pyqtSlot(bool)
    def on_checkBox_grupeer_toggled(self, checked):
        """
        Add/remove Grupeer to list of platforms.

        Args:
            checked (bool): if True add Grupeer, if False remove Grupeer

        """
        if checked:
            self.platforms.add('Grupeer')
        else:
            self.platforms.remove('Grupeer')

    @pyqtSlot(bool)
    def on_checkBox_dofinance_toggled(self, checked):
        """
        Add/remove Dofinance to list of platforms.

        Args:
            checked (bool): if True add Dofinance, if False remove Dofinance

        """
        if checked:
            self.platforms.add('DoFinance')
        else:
            self.platforms.remove('DoFinance')

    @pyqtSlot(bool)
    def on_checkBox_iuvo_toggled(self, checked):
        """
        Add/remove Iuvo to list of platforms.

        Args:
            checked (bool): if True add Iuvo, if False remove Iuvo

        """
        if checked:
            self.platforms.add('Iuvo')
        else:
            self.platforms.remove('Iuvo')

    @pyqtSlot(bool)
    def on_checkBox_peerberry_toggled(self, checked):
        """
        Add/remove Peerberry to list of platforms.

        Args:
            checked (bool): if True add Peerberry, if False remove Peerberry

        """
        if checked:
            self.platforms.add('PeerBerry')
        else:
            self.platforms.remove('PeerBerry')

    @pyqtSlot(bool)
    def on_checkBox_mintos_toggled(self, checked):
        """
        Add/remove Mintos to list of platforms.

        Args:
            checked (bool): if True add Mintos, if False remove Mintos

        """
        if checked:
            self.platforms.add('Mintos')
        else:
            self.platforms.remove('Mintos')

    @pyqtSlot(bool)
    def on_checkBox_robocash_toggled(self, checked):
        """
        Add/remove Robocash to list of platforms.

        Args:
            checked (bool): if True add Robocash, if False remove Robocash

        """
        if checked:
            self.platforms.add('Robocash')
        else:
            self.platforms.remove('Robocash')

    @pyqtSlot(bool)
    def on_checkBox_estateguru_toggled(self, checked):
        """
        Add/remove Estateguru to list of platforms.

        Args:
            checked (bool): if True add Estateguru, if False remove Estateguru

        """
        if checked:
            self.platforms.add('Estateguru')
        else:
            self.platforms.remove('Estateguru')

    @pyqtSlot(bool)
    def on_checkBox_swaper_toggled(self, checked):
        """
        Add/remove Swaper to list of platforms.

        Args:
            checked (bool): if True add Swaper, if False remove Swaper

        """
        if checked:
            self.platforms.add('Swaper')
        else:
            self.platforms.remove('Swaper')

    @pyqtSlot(bool)
    def on_checkBox_twino_toggled(self, checked):
        """
        Add/remove Twino to list of platforms.

        Args:
            checked (bool): if True add Twino, if False remove Twino

        """
        if checked:
            self.platforms.add('Twino')
        else:
            self.platforms.remove('Twino')

    @pyqtSlot(str)
    def on_comboBox_start_month_activated(self, month):
        """
        Update start date if the user changed start month in the combo box.

        Args:
            month (str): short month name chosen by the user in the combo box

        """
        self.start_month = int(wd.short_month_to_nbr(month))
        self.set_start_date()

    @pyqtSlot(str)
    def on_comboBox_start_year_activated(self, year):
        """
        Update start date if the user changed start year in the combo box.

        Args:
            year (str): year chosen by the user in the combo box

        """
        self.start_year = int(year)
        self.set_start_date()

    @pyqtSlot(str)
    def on_comboBox_end_month_activated(self, month):
        """
        Update end date if the user changed end month in the combo box.

        Args:
            month (str): short month name chosen by the user in the combo box

        """
        self.end_month = int(wd.short_month_to_nbr(month))
        self.set_end_date()

    @pyqtSlot(str)
    def on_comboBox_end_year_activated(self, year):
        """
        Update end date if the user changed end year in the combo box.

        Args:
            year (str): year chosen by the user in the combo box

        """
        self.end_year = int(year)
        self.set_end_date()

    @pyqtSlot()
    def on_pushButton_start_clicked(self):
        """
        Start evaluation for selected P2P platforms and the given date range.

        The evaluation will be done by a worker thread in class WorkerThread.
        Progress is tracked in ProgressWindow.

        """
        # Check that start date is before end date
        if self.start_date > self.end_date:
            QMessageBox.warning(
                self, 'Startdatum liegt nach Enddatum!',
                'Das Startdatum darf nicht nach dem Enddatum liegen!')
            return

        # Check that at least one platform is selected
        if not self.platforms:
            QMessageBox.warning(
                self, 'Keine P2P Plattform ausgewählt!',
                'Bitte wähle mindestens eine P2P Plattform aus')
            return

        # Check if download directory exists, if not create it
        dl_location = './p2p_downloads'
        if not os.path.isdir(dl_location):
            os.makedirs(dl_location)

        # Get credentials from user/keyring for all selected platforms
        for platform in self.platforms:
            self.credentials[platform] = get_credentials(platform)

        # Set up and start worker thread
        worker = self.setup_worker_thread()
        worker.start()

        # Open progress window
        self.progress_window = ProgressWindow()
        self.progress_window.exec_()

        # Abort the worker thread if user clicked the cancel button
        if self.progress_window.result() == 0:
            worker.abort = True

    def setup_worker_thread(self) -> 'WorkerThread':
        """
        Setup the worker thread and its attributes.

        Returns:
            WorkerThread: handle of the worker thread

        """
        worker = WorkerThread(
            self.platforms, self.credentials, self.start_date, self.end_date,
            self.output_file)
        worker.update_progress_bar.connect(self.update_progress_bar)
        worker.update_progress_text.connect(self.update_progress_text)
        return worker

    def update_progress_bar(self, value):
        """
        Update the progress bar in ProgressWindow to new value.

        Args:
            value (float): value of the progress bar, between 0 and 100

        """
        if not 0 <= value <= 100:
            error_message = ('Fortschrittsindikator beträgt: {0}. Er muss '
                             'zwischen 0 und 100 liegen!'.format(value))
            QMessageBox.warning(
                self, 'Fehler!', error_message)
            return

        self.progress_window.progressBar.setValue(value)

    def update_progress_text(self, txt, color):
        """
        Append a new line to the progress text in ProgressWindow.

        Args:
            txt (str): string to add to progress text
            color (QColor): color in which the message should be displayed

        """
        self.progress_window.progressText.setTextColor(color)
        self.progress_window.progressText.append(txt)

    @pyqtSlot(str)
    def on_lineEdit_output_file_textChanged(self, file_name):
        """
        Update location where the results file should be saved.

        Args:
            file_name (str): file name entered by the user

        """
        QLineEdit.setText(self.lineEdit_output_file, file_name)

    @pyqtSlot()
    def on_pushButton_file_chooser_clicked(self):
        """
        Open dialog window for changing the save location of the results file.
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.output_file, _ = QFileDialog.getSaveFileName(
            self, "Ausgabedatei wählen", self.output_file,
            "MS Excel Dateien (*.xlsx)", options=options)
        if self.output_file:
            # The file name must include xlsx file format. Otherwise the Excel
            # writer will crash later.
            if not self.output_file.endswith('.xlsx'):
                self.output_file = self.output_file + '.xlsx'
            self.on_lineEdit_output_file_textChanged(self.output_file)

    @pyqtSlot(bool)
    def on_checkBox_select_all_toggled(self, checked):
        """
        Toggle/untoggle all P2P platforms.

        Args:
            checked (bool): if True toggle all check boxes, if False untoggle
                all check boxes

        """
        for check_box in self.groupBox_platforms.findChildren(QCheckBox):
            check_box.setChecked(checked)

class WorkerThread(QThread):

    """
    Worker thread to offload calls to p2p_webdriver, p2p_parser, p2p_results.

    This class is responsible for accessing the P2P platform methods in
    p2p_webdriver and to prepare the results. The main reason for separating
    the calls to p2p_webdriver, p2p_parser and p2p_results from the main thread
    is to keep the GUI responsive while the webdriver is working.

    """

    # Signals for communicating with the MainWindow
    update_progress_bar = pyqtSignal(float)
    update_progress_text = pyqtSignal(str, QColor)

    # Colors for text output
    BLACK = QColor(0, 0, 0)
    RED = QColor(100, 0, 0)

    def __init__(
            self, platforms: AbstractSet[str],
            credentials: Mapping[str, Tuple[str, str]],
            start_date: date, end_date: date, output_file: str,
            parent=None) -> None:
        """
        Constructor.

        Args:
            platforms (set[str]): set containing the names of all selected P2P
                platforms
            credentials (dict[str, tuple[str, str]]): keys are the names of the
                P2P platforms, values are tuples with (username, password)
            start_date (datetime.date): start of date range for which the
                account statements should be generated.
            end_date (datetime.date): end of date range for which the
                account statements should be generated.
            output_file (str): name of the Excel file (including absolute path)
                to which the results should be written.

        Keyword Args:
            parent (QThread): reference to the parent thread

        """
        super(WorkerThread, self).__init__(parent)
        self.platforms = platforms
        self.credentials = credentials
        self.start_date = start_date
        self.end_date = end_date
        self.output_file = output_file
        self.abort = False

    def get_p2p_function(self, platform: str) -> wd.OpenSelenium:
        """
        Helper method to get the name of the appropriate webdriver function.

        Args:
            platform (str): name of the P2P platform

        Returns:
            OpenSelenium: p2p_webdriver.open_selenium_* function for handling
                this P2P platform or None if the function cannot be found

        """
        try:
            func = getattr(wd, 'open_selenium_'+platform.lower())
        except AttributeError:
            error_message = (
                'Funktion zum Öffnen von {0} konnte nicht gefunden werden. '
                'Ist p2p_webdriver.py vorhanden?'.format(platform))
            self.update_progress_text.emit(error_message, self.RED)
            return None
        else:
            return func

    def get_p2p_parser(self, platform: str) -> p2p_parser.Parser:
        """
        Helper method to get the name of the appropriate parser.

        Args:
            platform (str): name of the P2P platform

        Returns:
            Parser: p2p_parser.* function for parsing this P2P platform or
                None if the function cannot be found

        """
        try:
            parser = getattr(p2p_parser, platform.lower())
        except AttributeError:
            error_message = (
                'Parser für {0} konnte nicht gefunden werden. '
                'Ist p2p_parser.py vorhanden?'.format(platform))
            self.update_progress_text.emit(error_message, self.RED)
            return None
        else:
            return parser

    def ignore_platform(self, platform: str, error_msg: str) -> None:
        """
        Helper method for printing ignore and error message to GUI.

        Args:
            platform (str): name of the P2P platform
            error_msg (str): error message

        """
        self.update_progress_text.emit(error_msg, self.RED)
        self.update_progress_text.emit(
            '{0} wird ignoriert!'.format(platform), self.RED)

    def parse_result(
            self, platform: str, parser: p2p_parser.Parser,
            list_of_dfs: list) -> list:
        """
        Helper method for calling the parser and appending the dataframe list.

        Args:
            platform (str): name of the P2P platform
            parser (p2p_parser.Parser): parser method for parsing results
            list_of_dfs (list(pd.DataFrame)): list of DataFrames, one DataFrame
                for each successfully parsed P2P platform

        Returns:
            list(pd.DataFrame): if successful the provided list_of_dfs with one
                DataFrame appended, if not then the original list_of_dfs is
                returned

        """
        try:
            df = parser()[0]
            list_of_dfs.append(df)
        except FileNotFoundError:
            error_msg = ('Der heruntergeladene {0}-Kontoauszug konnte nicht '
                         'gefunden werden!'.format(platform))
            self.ignore_platform(platform, error_msg)
            return list_of_dfs
        except XLRDError:
            error_msg = ('Der heruntergeladene {0}-Kontoauszug ist beschädigt!'
                         ''.format(platform))
            self.ignore_platform(platform, error_msg)
            return list_of_dfs
        else:
            if parser()[1]:
                warning_msg = ('{0}: unbekannter Cashflow-Typ wird im '
                               'Ergebnis ignoriert: {1}'
                               ''.format(platform, parser()[1]))
                self.update_progress_text.emit(warning_msg, self.RED)

        return list_of_dfs

    def run_platform(self, platform: str, func: wd.OpenSelenium) -> bool:
        """
        Helper method for calling the open_selenium_* function.

        Args:
            platform (str): name of the P2P platform
            func (wd.OpenSelenium): function to run

        Returns:
            bool: True if function was run without errors, False otherwise.

        """
        success = False
        if self.credentials[platform] is None:
            self.update_progress_text.emit(
                'Keine Zugangsdaten für {0} vorhanden!'.format(platform),
                self.RED)
            return False

        self.update_progress_text.emit(
            'Start der Auswertung von {0}...'.format(platform), self.BLACK)
        try:
            success = func(
                self.start_date, self.end_date, self.credentials[platform])
        except RuntimeError as err:
            self.ignore_platform(platform, str(err))
            return False
        except RuntimeWarning as warning:
            self.update_progress_text.emit(str(warning), self.RED)
            # Continue anyway

        return success

    def run(self):
        """
        Get and output results from all selected P2P platforms.

        Iterates over all selected P2P platforms, gets the results from
        p2p_webdriver and outputs the results. After each platform the progress
        bar is increased.

        """
        list_of_dfs = []
        progress = 0
        # Distribute 95% evenly across all selected platforms
        # The last 5 percent are for preparing the results
        step = 95/len(self.platforms)

        for platform in self.platforms:
            if self.abort:
                return

            func = self.get_p2p_function(platform)
            if func is None:
                continue

            success = self.run_platform(platform, func)

            if success:
                if self.abort:
                    return

                progress += step
                self.update_progress_bar.emit(progress)
                self.update_progress_text.emit(
                    '{0} erfolgreich ausgewertet!'.format(platform),
                    self.BLACK)

                parser = self.get_p2p_parser(platform)
                if parser is None:
                    continue

                list_of_dfs = self.parse_result(platform, parser, list_of_dfs)

        if self.abort:
            return

        df_result = p2p_results.combine_dfs(list_of_dfs)

        if not p2p_results.show_results(
                df_result, self.start_date, self.end_date, self.output_file):
            self.update_progress_text.emit(
                'Keine Ergebnisse vorhanden', self.RED)

        self.update_progress_bar.emit(100)
