# -*- coding: utf-8 -*-
# Copyright 2018-19 Niko Sandschneider

"""
Module for getting and saving credentials in the system keyring / from the user.

"""
import keyring
from typing import Optional, Tuple

from easyp2p.ui.credentials_window import CredentialsWindow


def get_credentials(platform: str) -> Optional[Tuple[str, str]]:
    """
    Get credentials for P2P platform from keyring or user.

    If a keyring exists, try to get credentials from it. If not or if they
    cannot be found, ask user for credentials.

    Args:
        platform: Name of the P2P platform

    Returns:
        Tuple (username, password) on success, None otherwise

    """
    _ask_for_credentials = False

    if keyring.get_keyring():
        try:
            username = keyring.get_password(platform, 'username')
            password = keyring.get_password(platform, username)
        except TypeError:
            # Either username or password were not found in the keyring
            _ask_for_credentials = True
    else:
        _ask_for_credentials = True

    if _ask_for_credentials:
        (username, password) = get_credentials_from_user(platform)
        if not username or not password:
            return None

    return (username, password)


def get_credentials_from_user(
        platform: str, save_in_keyring: bool = False) \
        -> Tuple[Optional[str], Optional[str]]:
    """
    Ask user for P2P platform credentials.

    Args:
        platform: Name of the P2P platform

    Returns:
        Tuple (username, password) on success, (None, None) otherwise

    """
    username, password = None, None
    while not username or not password:
        credentials_window = CredentialsWindow(platform, save_in_keyring)

        if not credentials_window.exec_():
            # User clicked the Cancel button
            return (None, None)

        username = credentials_window.line_edit_username.text()
        password = credentials_window.line_edit_password.text()

    return (username, password)