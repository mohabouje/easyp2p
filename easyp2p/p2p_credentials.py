# -*- coding: utf-8 -*-
#  Copyright (c) 2018-2020 Niko Sandschneider

"""
Module for getting and saving credentials in the system keyring / from the user.

"""
from typing import Optional, Tuple

import keyring
from keyring.errors import PasswordDeleteError
from PyQt5.QtCore import QCoreApplication

from easyp2p.ui.credentials_window import CredentialsWindow

_translate = QCoreApplication.translate


def keyring_exists() -> bool:
    """
    Check if there is a keyring available.

    Returns:
        True if a keyring is found, False if not

    """
    return keyring.get_keyring()


def get_credentials_from_keyring(platform):
    """
    Try to get credentials for platform from keyring.

    Args:
        platform: Name of the P2P platform

    Returns:
        Tuple (username, password) or None if credentials were not found in the
        keyring.

    """
    username, password = None, None

    if keyring.get_keyring():
        username = keyring.get_password(platform, 'username')
        if username is not None:
            password = keyring.get_password(platform, username)

    if username is None or password is None:
        return None

    return username, password


def get_credentials_from_user(
        platform: str, save_in_keyring: bool = False) \
        -> Tuple[Optional[str], Optional[str]]:
    """
    Ask user for P2P platform credentials.

    Args:
        platform: Name of the P2P platform
        save_in_keyring: If True the save_in_keyring checkbox will be
            checked and disabled. Default is False.

    Returns:
        Tuple (username, password)

    """
    cred_window = CredentialsWindow(
        platform, keyring.get_keyring(), save_in_keyring)
    cred_window.exec_()

    if cred_window.save_in_keyring:
        if not save_platform_in_keyring(
                platform, cred_window.username, cred_window.password):
            cred_window.warn_user(
                _translate('p2p_credentials', 'Saving in keyring failed!'),
                _translate(
                    'p2p_credentials', 'Saving password in keyring was not '
                    'successful!'))

    return cred_window.username, cred_window.password


def get_password_from_keyring(platform: str, username: str) -> Optional[str]:
    """
    Get password for platform:username from keyring.

    Args:
        platform: Name of the P2P platform
        username: Username for which to get the password

    Returns:
        Password or None if no password was found for username

    """
    return keyring.get_password(platform, username)


def delete_platform_from_keyring(platform: str) -> bool:
    """
    Delete credentials for platform from keyring.

    Args:
        platform: Name of the P2P platform

    Returns:
        True on success, False on failure

    Raises:
        RuntimeError: If 'username' for platform cannot be found in the keyring

    """
    try:
        username = keyring.get_password(platform, 'username')
        if not username:
            raise RuntimeError(
                _translate(
                    'p2p_credentials', f'{platform} was not found in keyring!'))
        keyring.delete_password(platform, username)
        keyring.delete_password(platform, 'username')
    except PasswordDeleteError:
        return False
    return True


def save_platform_in_keyring(
        platform: str, username: str, password: str) -> bool:
    """
    Save credentials for platform in keyring.

    Args:
        platform: Name of the P2P platform
        username: Username for platform
        password: Password for platform

    Returns:
        True on success, False on failure

    Raises:
        RuntimeError: If username == 'username'

    """
    # We use 'username' to save the user name of the platform, thus it cannot be
    # used as a "normal" user name. This is only a hypothetical problem since
    # P2P platforms use email addresses as user names
    if username == 'username':
        raise RuntimeError(
            _translate(
                'p2p_credentials', 'User name "username" is not allowed!'))

    try:
        keyring.set_password(platform, 'username', username)
        keyring.set_password(platform, username, password)
    except keyring.errors.PasswordSetError:
        return False
    return True
