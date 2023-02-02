#!/usr/bin/env python3
"""Encrypts a password"""


import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password"""
    encoded = password.encode('utf-8')
    return bcrypt.hashpw(encoded, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """checks if a password is valid"""
    encoded = password.encode('utf-8')
    return bcrypt.checkpw(encoded, hashed_password)
