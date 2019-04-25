# -*- coding: utf-8 -*-
# Copyright 2018-19 Niko Sandschneider
# pylint: disable=invalid-name

"""Module implementing CredentialsWindow."""
from typing import Optional, Tuple

import keyring
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QMessageBox, QWidget

from easyp2p.ui.Ui_credentials_window import Ui_CredentialsWindow


# TODO: add methods for changing/deleting credentials
class CredentialsWindow(QDialog, Ui_CredentialsWindow):

    """
    Class for getting P2P platform login credentials from user or keyring.

    CredentialWindow defines a dialog for getting P2P platform credentials
    from a keyring or by user input if the credentials cannot be found in the
    keyring.

    """

    def __init__(self, platform: str, parent: QWidget = None) -> None:
        """
        Constructor.

        Args:
            platform: Name of the P2P platform

        Keyword Args:
            parent: Reference to the parent widget

        """
        super(CredentialsWindow, self).__init__(parent)
        self.setupUi(self)
        self.label_platform.setText('Bitte geben Sie Benutzername und '
                                    'Passwort für {0} ein:'.format(platform))

    @pyqtSlot()
    def on_button_box_accepted(self) -> None:
        """Send accept() signal if OK button is clicked."""
        self.accept()

    @pyqtSlot()
    def on_button_box_rejected(self) -> None:
        """Send reject() signal if Cancel button is clicked."""
        self.reject()


def get_credentials(platform: str) -> Optional[Tuple[str, str]]:
    """
    Get credentials for P2P platform from keyring or from user input.

    If a keyring exists, try to get credentials from it. If not or if they
    cannot be found, ask user for credentials. If the save_in_keyring check box
    is toggled, the supplied credentials will be saved in the keyring.

    Args:
        platform: Name of the P2P platform

    Returns:
        Tuple (username, password) on success, None if user clicks Cancel

    """
    _done = False
    _ask_for_credentials = False
    _save_in_keyring = False

    while not _done:

        if keyring.get_keyring():
            try:
                username = keyring.get_password(platform, 'username')
                password = keyring.get_password(platform, username)
                _done = True
            except TypeError:
                # Either username or password were not found in the keyring
                _ask_for_credentials = True
        else:
            _ask_for_credentials = True

        if _ask_for_credentials:
            credentials_window = CredentialsWindow(platform)
            if not credentials_window.exec_():
                # User clicked the Cancel button
                return None
            username = credentials_window.line_edit_username.text()
            password = credentials_window.line_edit_password.text()

            if not username or not password:
                QMessageBox.warning(
                    credentials_window, 'Felder nicht ausgefüllt', 'Bitte '
                    'füllen Sie die Felder für Benutzername und Passwort aus!')
            else:
                _done = True
                _save_in_keyring = (
                    credentials_window.check_box_save_in_keyring.isChecked())

    if _save_in_keyring:
        if not save_credentials(platform, username, password):
            QMessageBox.warning(
                credentials_window, 'Speichern im Keyring fehlgeschlagen!',
                'Speichern des Passworts im Keyring war leider nicht '
                'erfolgreich!')

    return (username, password)

def save_credentials(platform: str, username: str, password: str) -> bool:
    """
    Save credentials for P2P platform in keyring.

    If a keyring exists, try to save credentials in it. If not or if they
    cannot be found, ask user for credentials. If the save_in_keyring check box
    is toggled, the supplied credentials will be saved in the keyring.

    Args:
        platform: Name of P2P platform
        username: Username for P2P platform
        password: Password for P2P platform

    Returns:
        True if credentials were saved successfully, False if not

    """
    if keyring.get_keyring():
        try:
            keyring.set_password(platform, 'username', username)
            keyring.set_password(platform, username, password)
            return True
        except keyring.errors.PasswordSetError:
            return False

    return False
