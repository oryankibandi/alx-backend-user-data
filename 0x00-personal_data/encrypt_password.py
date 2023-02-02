#!/usr/bin/env python3
"""Encrypts a password"""

import typing
import bcrypt


def hash_password(password: str) -> typing.ByteString:
    """Hashes a password"""
    encoded = password.encode('utf-8')
    return bcrypt.hashpw(encoded, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """checks if a password is valid"""
    encoded = password.encode('utf-8')
    return bcrypt.checkpw(encoded, hashed_password)
