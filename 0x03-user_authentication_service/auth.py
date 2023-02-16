#!/usr/bin/env python3

import bcrypt
import base64
import uuid
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound, InvalidRequestError


def _hash_password(password: str) -> bytes:
    """hashes a password"""
    encoded_pw = base64.b64encode(bytes(password, 'utf-8'))
    return bcrypt.hashpw(encoded_pw, bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generates a UUID"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registers a user"""

        existing_user = self._db.find_user_by(email=email)
        if existing_user:
            raise ValueError(f"User {email} already exists")
        else:
            hashed_pwd = _hash_password(password)
            new_user = self._db.add_user(email, hashed_pwd)

            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """validates credentials"""
        try:
            existing = self._db.find_user_by(email=email)

            if bcrypt.checkpw(password, _hash_password(password)):
                return True
            else:
                return False
        except:
            return False

    def create_session(self, email: str) -> str:
        """creates a session ID"""
        existing_user: User = self._db.find_user_by(email=email)
        existing_user.session_id = _generate_uuid()
        self._db.__session.commit()

        return existing_user.session_id

    def get_user_from_session_id(self, session_id: str) -> User | None:
        """Gets a user from session_id"""
        if session_id is None:
            return None

        user = self._db.find_user_by(session_id=session_id)

        if user is None:
            return None
        else:
            return user

    def destroy_session(self, user_id: str) -> None:
        """Destroys a user session"""
        self._db.update_user(user_id, session_id=None)

        return None

    def get_reset_password_token(self, email: str) -> str:
        """generates a reset token"""
        user = self._db.find_user_by(email=email)
        if user is None:
            raise ValueError
        else:
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)

            return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates a users password"""
        user = self._db.find_user_by(reset_token=reset_token)

        if user is None:
            raise ValueError
        else:
            hashed_pwd = self.__hash__(password)
            self._db.update_user(
                user.id, hashed_password=str(hashed_pwd),
                reset_token=None)
