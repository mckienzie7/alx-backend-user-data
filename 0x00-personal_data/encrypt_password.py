#!/usr/bin/env python3
"""
Module for encrypting passwords.
"""
import bcrypt
from typing import Union


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt with a randomly generated salt.
    Args:
        password: The password to be hashed.
    Returns:
        bytes: The salted, hashed password as a byte string.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Checks if a password matches its hashed version.
    Args:
        hashed_password: The hashed password stored in the database.
        password: The password provided by the user to be checked.
    Returns:
        bool: True if the provided password matches the
        hashed password, False otherwise.
    """
    return bcrypt.checkpw(
        password.encode('utf-8'), hashed_password
    )
