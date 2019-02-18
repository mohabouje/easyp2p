# -*- coding: utf-8 -*-
# Copyright 2018-19 Niko Sandschneider

"""
Module implementing P2PPlatform, a class representing a P2P platform.

This module defines the P2PPlatform class. It contains code for performing log
in, opening the account statement page and downloading the account statement.
It relies mainly on functionality provided by the Selenium webdriver. easyp2p
uses Chromedriver as webdriver.

"""

from datetime import date
import glob
from pathlib import Path
import os
import time
from typing import cast, Mapping, Optional, Tuple

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains

import p2p_helper


class P2PPlatform:

    """
    Representation of P2P platform including required methods for interaction.

    Represents a P2P platform and the required methods for login/logout,
    generating and downloading account statements.

    """

    def __init__(
            self, name: str, urls: Mapping[str, str],
            logout_wait_until: bool,
            logout_locator: Optional[Tuple[str, str]] = None,
            hover_locator: Optional[Tuple[str, str]] = None) -> None:
        """
        Constructor of P2P class.

        Args:
            name (str): Name of the P2P platform
            urls (dict[str, str]): Dictionary with URLs for login page
                (key: 'login'), account statement page (key: 'statement')
                and optionally logout page (key: 'logout')
            logout_wait_until (bool): Expected condition in case
                of successful logout.

        Keyword Args:
            logout_locator (tuple[str, str]): locator of logout web element.
            hover_locator (tuple[str, str]): locator of web element where the
                mouse needs to hover in order to make logout button visible.

        Throws:
            RuntimeError: if no URL for login or statement page is provided.

        """
        self.name = name
        self.urls = urls
        self.logout_wait_until = logout_wait_until
        self.logout_locator = logout_locator
        self.hover_locator = hover_locator
        # self.driver will be initialized in __enter__ method to make sure it
        # is always closed again by __exit__
        self.driver = cast(webdriver.Chrome, None)
        self.logged_in = False

        # Make sure URLs for login and statement page are provided
        if 'login' not in urls:
            raise RuntimeError('Keine Login-URL für {0} '
                               'vorhanden!'.format(self.name))
        if 'statement' not in urls:
            raise RuntimeError('Keine Kontoauszug-URLs für {0} '
                               'vorhanden!'.format(self.name))

    def __enter__(self) -> 'P2P':
        """
        Start of context management protocol.

        Returns:
            P2P: instance of P2P class

        Throws:
            RuntimeError: if neither logout URL or a locator for the logout
                button are provided.

        """
        self.init_webdriver()
        return self

    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        """End of context management protocol."""

        if self.logged_in:
            if 'logout' in self.urls:
                self.logout_by_url(self.logout_wait_until)
            elif self.logout_locator is not None:
                self.logout_by_button(
                    self.logout_locator, self.logout_wait_until,
                    hover_locator=self.hover_locator)
            else:
                raise RuntimeError(
                    '{0}: Keine Methode für Logout vorhanden!'
                    .format(self.name))

            self.logged_in = False

        self.driver.close()
        if exc_type:
            raise exc_type(exc_value)

    def init_webdriver(self) -> None:
        """
        Initialize Chromedriver as webdriver.

        This function initializes Chromedriver as webdriver, sets the
        default download location to p2p_downloads relative to the current
        working directory and opens a new maximized browser window.

        """
        options = webdriver.ChromeOptions()
#        options.add_argument("--headless")
#        options.add_argument("--window-size=1920,1200")
        dl_location = os.path.join(os.getcwd(), 'p2p_downloads')
        prefs = {"download.default_directory": dl_location}
        options.add_experimental_option("prefs", prefs)

        try:
            driver = webdriver.Chrome(options=options)
        except WebDriverException:
            raise RuntimeError('Chromedriver konnte nicht gefunden werden!')

        driver.maximize_window()
        self.driver = driver

    def log_into_page(
            self, name_field: str, password_field: str,
            credentials: Tuple[str, str], wait_until: bool,
            login_locator: Tuple[str, str] = None,
            fill_delay: float = 0) -> None:
        """
        Log into the P2P platform with provided user name/password.

        This function performs the login procedure for the P2P site.
        It opens the login page and fills in user name and password.
        Some P2P sites only show the user name and password field after
        clicking a button whose locator can be provided by the optional
        login_locator. Some P2P sites (e.g. Swaper) also require a small delay
        between filling in name and password. Otherwise it can
        sometimes happen that the password is mistakenly written
        to the name field, too.

        Args:
            name_field (str): name of web element where the user name
                has to be entered.
            password_field (str): name of web element where the password
                has to be entered.
            credentials (tuple[str, str]): login information: (username,
                password)
            wait_until (bool): Expected condition in case of
                success.

        Keyword Args:
            login_locator (tuple[str, str]): locator of web element which has
                to be clicked in order to open login form.
            fill_delay (float): a small delay between filling in password
                and user name fields.

        Throws:
            RuntimeError: - if login or password fields cannot be found
                          - if loading the page takes too long

        """
        # Open the login page
        try:
            self.driver.get(self.urls['login'])

            if login_locator is not None:
                self.wdwait(EC.element_to_be_clickable(login_locator))
                self.driver.find_element(*login_locator).click()

            # Make sure that the correct URL was loaded
            if self.driver.current_url != self.urls['login']:
                raise RuntimeError(
                    'Die {0}-Webseite konnte nicht geladen werden.'
                    .format(self.name))
        except TimeoutException:
            raise RuntimeError(
                'Das Laden der {0}-Webseite hat zu lange gedauert.'
                .format(self.name))

        # Enter credentials in name and password field
        try:
            self.wdwait(EC.element_to_be_clickable((By.NAME, name_field)))
            elem = self.driver.find_element_by_name(name_field)
            elem.clear()
            elem.send_keys(credentials[0])
            time.sleep(fill_delay)
            elem = self.driver.find_element_by_name(password_field)
            elem.clear()
            elem.send_keys(credentials[1])
            elem.send_keys(Keys.RETURN)
            # Login currently takes a long time for Twino, thus increase the
            # waiting time for now. They promised an web site update for
            # 28/01/2018 which should fix this issue.
            if self.name == 'Twino':
                self.wdwait(wait_until, delay=10)
            else:
                self.wdwait(wait_until)
        except NoSuchElementException:
            raise RuntimeError(
                'Benutzername/Passwort-Felder konnten nicht auf der '
                '{0}-Loginseite gefunden werden!'.format(self.name))
        except TimeoutException:
            raise RuntimeError(
                '{0}-Login war leider nicht erfolgreich. Passwort korrekt?'
                .format(self.name))

        self.logged_in = True

    def open_account_statement_page(
            self, title: str, check_locator: Tuple[str, str]) -> None:
        """
        Open account statement page of the P2P platform.

        This function opens the account statement page of the P2P site.
        The URL of the account statement page is provided as an
        attribute of the P2P class.

        Args:
            title (str): (part of the) window title of the account statement
                page.
            check_locator (tuple[str, str]): locator of a web element which
                must be present if the account statement page loaded
                successfully.

        Throws:
            RuntimeError: - if title of the page is not equal to provided one
                          - if loading of page takes too long

        """
        try:
            self.driver.get(self.urls['statement'])
            self.wdwait(EC.presence_of_element_located(check_locator))
            assert title in self.driver.title
        except (AssertionError, TimeoutException):
            raise RuntimeError(
                '{0}-Kontoauszugsseite konnte nicht geladen werden!'
                ''.format(self.name))

    def logout_by_button(
            self, logout_locator: Tuple[str, str],
            wait_until: bool,
            hover_locator: Optional[Tuple[str, str]] = None) -> None:
        """
        Logout of P2P platform using the provided logout button.

        This function performs the logout procedure for P2P sites
        where a button needs to be clicked to logout. For some sites the
        button only becomes clickable after hovering over a certain element.
        This element is provided by the optional hover_elem variable.

        Args:
            logout_locator (tuple[str, str]): locator of logout button.
            wait_until (bool): Expected condition in case of
                successful logout.

        Keyword Args:
            hover_locator (str): locator of web element over which the mouse
                needs to hover in order to make the logout button visible.

        Throws:
            RuntimeWarning: if loading of page takes too long or the download
                button cannot be found.

        """
        try:
            if hover_locator is not None:
                elem = self.driver.find_element(*hover_locator)
                hover = ActionChains(self.driver).move_to_element(elem)
                hover.perform()
                self.wdwait(EC.element_to_be_clickable(logout_locator))

            self.driver.find_element(*logout_locator).click()
            self.wdwait(wait_until)
        except (NoSuchElementException, TimeoutException):
            raise RuntimeWarning(
                '{0}-Logout war nicht erfolgreich!'.format(self.name))

    def logout_by_url(
            self, wait_until: bool) -> None:
        """
        Logout of P2P platform using the provided URL.

        This function performs the logout procedure for P2P sites
        where the logout page can by accessed by URL. The URL itself is
        provided in the urls dict attribute of the P2P class.

        Args:
            wait_until (bool): Expected condition in case of
                successful logout

        Throws:
            RuntimeWarning: if loading of page takes too long

        """
        try:
            self.driver.get(self.urls['logout'])
            self.wdwait(wait_until)
        except TimeoutException:
            raise RuntimeWarning(
                '{0}-Logout war nicht erfolgreich!'.format(self.name))

    def generate_statement_direct(
            self, date_range: Tuple[date, date],
            start_locator: Tuple[str, str], end_locator: Tuple[str, str],
            date_format: str, wait_until: bool = None,
            submit_btn_locator: Tuple[str, str] = None) -> None:
        """
        Generate acc. statement for platforms where date fields can be edited.

        For P2P sites where the two date range fields for account statement
        generation can be edited directly. The function will locate the two
        date fields, enter start and end date and then start the account
        statement generation.

        Args:
            date_range (tuple(date, date)): date range
                (start_date, end_date) for which the account statement must
                be generated.
            start_locator (tuple[str, str]): locator of field where the start
                date needs to be entered.
            end_element (tuple[str, str]): locator of field where the end date
                needs to be entered.
            date_format (str): date format.

        Keyword Args:
            wait_until (bool): Expected condition in case of
                successful account statement generation.
            submit_btn_locator (tuple[str, str]): locator of button which needs
                to clicked to start account statement generation. Not all P2P
                platforms require this.

        Throws:
            RuntimeError: - if a web element cannot be found
                          - if the generation of the account statement
                            takes too long

        """
        try:
            date_from = self.driver.find_element(*start_locator)
            date_from.send_keys(Keys.CONTROL + 'a')
            date_from.send_keys(date.strftime(date_range[0], date_format))

            try:
                date_to = self.driver.find_element(*end_locator)
                date_to.click()
                date_to.send_keys(Keys.CONTROL + 'a')
                date_to.send_keys(date.strftime(date_range[1], date_format))
                date_to.send_keys(Keys.RETURN)
            except StaleElementReferenceException:
                # Some P2P sites refresh the page after a change
                # which leads to this exception
                date_to = self.driver.find_element(*end_locator)
                date_to.send_keys(Keys.CONTROL + 'a')
                date_to.send_keys(date.strftime(date_range[0], date_format))

            if submit_btn_locator is not None:
                button = self.wdwait(EC.element_to_be_clickable(
                    submit_btn_locator))
                if self.name == 'Mintos':
                    # Mintos needs some time until the button really works
                    # TODO: find better fix
                    time.sleep(1)
                button.click()

            if wait_until is not None:
                self.wdwait(wait_until)
        except NoSuchElementException:
            raise RuntimeError('Generierung des {0}-Kontoauszugs konnte nicht '
                               'gestartet werden.'.format(self.name))
        except TimeoutException:
            raise RuntimeError(
                'Generierung des {0}-Kontoauszugs hat zu lange gedauert.'
                ''.format(self.name))

    def generate_statement_calendar(
            self, date_range: Tuple[date, date],
            default_dates: Tuple[date, date],
            arrows: Mapping[str, str],
            days_table: Mapping[str, object],
            calendar_locator: Tuple[Tuple[str, str], ...]) -> None:
        """
        Generate account statement by clicking days in a calendar.

        For P2P sites where the two date range fields for account
        statement generation cannot be edited directly, but must be
        clicked in a calendar. The function will locate the two calendars,
        determine how many clicks are necessary to get to the
        correct month, perform the clicks and finally locate and click
        the chosen day.

        Args:
            date_range (tuple(date, date)): date range
                (start_date, end_date) for which the account statement must
                be generated.
            default_dates (tuple[date, date]): the pre-filled
                default dates of the two date pickers.
            arrows (dict[str, str]): dictionary with three entries: class name
                of left arrows, class name of right arrows,
                tag name of arrows.
            days_table (dict[str, {str, bool}]): dictionary with four entries:
                class name of day table, id of day table, id of current day,
                is day contained in id?.
            calendar_locator (tuple[tuple[str, str], ...]): tuple containing
                locators for the two calendars. It must have either length 1
                or 2.

        Throws:
            RuntimeError: - if a web element cannot be found
                          - if the generation of the account statement
                            takes too long

        """
        try:
            # Identify the two calendars. If calendar_locator contains two
            # elements, those are the locators for each calendar. If it
            # contains only one element, this is the locator of a
            # datepicker list which contains both calendars.
            if len(calendar_locator) == 2:
                start_calendar = self.driver.find_element(*calendar_locator[0])
                end_calendar = self.driver.find_element(*calendar_locator[1])
            elif len(calendar_locator) == 1:
                datepicker = self.driver.find_elements(*calendar_locator[0])
                start_calendar = datepicker[0]
                end_calendar = datepicker[1]
            else:
                # This should never happen
                raise RuntimeError(
                    '{0}: Ungültiger Locator für Kalender übergeben'
                    .format(self.name))

            # How many clicks on the arrow buttons are necessary?
            start_calendar_clicks = p2p_helper.get_calendar_clicks(
                date_range[0], default_dates[0])
            end_calendar_clicks = p2p_helper.get_calendar_clicks(
                date_range[1], default_dates[1])

            # Identify the arrows for both start and end calendar
            left_arrows = self.driver.find_elements_by_xpath(
                "//{0}[@class='{1}']".format(
                    arrows['arrow_tag'], arrows['left_arrow_class']))
            right_arrows = self.driver.find_elements_by_xpath(
                "//{0}[@class='{1}']".format(
                    arrows['arrow_tag'], arrows['right_arrow_class']))

            # Set start_date
            self.set_date_in_calendar(
                start_calendar, date_range[0].day, start_calendar_clicks,
                left_arrows[0], right_arrows[0], days_table)

            # Set end_date
            self.set_date_in_calendar(
                end_calendar, date_range[1].day, end_calendar_clicks,
                left_arrows[1], right_arrows[1], days_table)

        except NoSuchElementException:
            raise RuntimeError('Generierung des {0}-Kontoauszugs konnte nicht '
                               'gestartet werden.'.format(self.name))
        except TimeoutException:
            raise RuntimeError('Generierung des {0}-Kontoauszugs hat zu lange '
                               'gedauert.'.format(self.name))

    def set_date_in_calendar(
            self, calendar_: WebElement, day: int, months: int,
            previous_month: WebElement, next_month: WebElement,
            days_table: Mapping[str, object]) -> None:
        """
        Find and click the given day in the provided calendar.

        Args:
            calendar_ (WebElement): web element which needs to be clicked
                in order to open the calendar
            day (int): day number of the target date
            months (int): how many months in the past/future
                (negative/positive) is the target date
            previous_month (WebElement): web element to switch calendar to the
                previous month
            next_month (WebElement): web element to switch calendar to the
                next month
            days_table (dict[str, {str, bool}]): dictionary with four entries:
                class name of day table, id of day table, id of current day,
                is day contained in id?.

        """
        # Open the calendar and wait until the buttons for changing the month
        # are visible
        calendar_.click()
        self.wdwait(EC.visibility_of(previous_month))

        # Switch the calendar to the given target month
        if months < 0:
            for _ in range(0, abs(months)):
                previous_month.click()
        elif months > 0:
            for _ in range(0, months):
                next_month.click()

        # Get table with all days of the selected month
        # If id_from_calendar is True the day number is contained in the id tag
        # Otherwise the days will be identified by the provided class name
        if days_table['id_from_calendar']:
            days_xpath = "//*[@{0}='{1}']//table//td".format(
                days_table['table_id'], calendar_.get_attribute('id'))
        else:
            days_xpath = "//*[@{0}='{1}']//table//td".format(
                days_table['table_id'], days_table['class_name'])
        all_days = self.driver.find_elements_by_xpath(days_xpath)

        # Find and click the target day
        for elem in all_days:
            if days_table['current_day_id'] == '':
                if elem.text == str(day):
                    elem.click()
            else:
                if (elem.text == str(day) and elem.get_attribute('class')
                        == days_table['current_day_id']):
                    elem.click()

    def download_statement(
            self, default_file_name: str, download_locator: Tuple[str, str],
            actions=None) -> None:
        """
        Download account statement by clicking the provided button.

        Downloads the generated account statement and checks
        if the download was successful. If the download was successful,
        it will also call the rename_statement function to rename
        the downloaded file to the file name chosen by the user.

        Args:
            default_file_name (str): default file name without path for account
                statement downloads, chosen by the P2P platform
            download_locator (tuple[str, str]): locator of the download button.

        Keyword Args:
            actions (str): 'move to element' or None: some P2P sites
                require that the mouse hovers over a certain element
                in order to make the download button clickable.

        Throws:
            RuntimeError: - if the download button cannot be found
                          - if the downloaded file cannot be found and there
                            is no active download
                          - if more than one active download of
                            default_file_name is found

        """
        # Get a list of all files named default_file_name since it contains
        # wildcards for some P2P platforms
        file_list = glob.glob('p2p_downloads/' + default_file_name)

        # Find and click the download button
        try:
            download_button = self.driver.find_element(*download_locator)

            if actions == 'move_to_element':
                action = ActionChains(self.driver)
                action.move_to_element(download_button).perform()

            download_button.click()
        except NoSuchElementException:
            raise RuntimeError(
                'Download des {0} Kontoauszugs konnte nicht gestartet werden.'
                .format(self.name))

        # Wait until download has finished
        _download_finished = False
        _waiting_time = 0
        max_waiting_time = 4
        while not _download_finished:
            new_file_list = glob.glob('p2p_downloads/' + default_file_name)
            if len(new_file_list) - len(file_list) == 1:
                _download_finished = True
            elif new_file_list == file_list:
                ongoing_downloads = glob.glob(
                    'p2p_downloads/{0}.crdownload'.format(default_file_name))
                if not ongoing_downloads and _waiting_time > max_waiting_time:
                    # If the download didn't start after more than
                    # max_waiting_time something has gone wrong.
                    raise RuntimeError(
                        'Download des {0}-Kontoauszugs wurde abgebrochen!'
                        .format(self.name))

                time.sleep(1)
                _waiting_time += 1
            else:
                # This should never happen
                raise RuntimeError(
                    'Mehr als ein aktiver Download des {0}-Kontoauszugs '
                    'gefunden!'.format(self.name))

        # Get actual file name of downloaded file
        file_name = [file for file in new_file_list if file not in file_list][0]
        self._rename_statement(file_name)

    def wdwait(
            self, wait_until: bool,
            delay: float = 5.0) -> WebElement:
        """
        Shorthand for WebDriverWait.

        Args:
            wait_until (bool): expected condition for which the
                webdriver should wait.

        Keyword Args:
            delay (float): maximal waiting time in seconds

        Returns:
            WebElement: WebElement which WebDriverWait waited for.

        """
        return WebDriverWait(self.driver, delay).until(wait_until)

    def _rename_statement(self, file_name: str) -> None:
        """
        Rename downloaded statement to default_file_name.

        Will rename the downloaded statement from the
        default name chosen by the P2P platform to
        default_file_name.

        Args:
            file_name (str): file name of the downloaded account statement

        Throws:
            RuntimeError: if the downloaded statement cannot be found

        """
        error_msg = (
            '{0}-Kontoauszug konnte nicht im Downloadverzeichnis gefunden '
            'werden.'.format(self.name))

        if file_name is None:
            raise RuntimeError(error_msg)

        try:
            os.rename(
                file_name, 'p2p_downloads/{0}_statement{1}'.format(
                    self.name.lower(), Path(file_name).suffix))
        except FileNotFoundError:
            raise RuntimeError(error_msg)
