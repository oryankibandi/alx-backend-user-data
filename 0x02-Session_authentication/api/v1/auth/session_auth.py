#!/usr/bin/env python3

import os
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """Session Authentication class

    Args:
        Auth (_type_): _description_
    """

    user_id_by_session_id = {}

    def __init__(self):
        """Initializes the instance
        """

    def create_session(self, user_id: str = None) -> str:
        """creates a sessionID for user_id

        Args:
            user_id (str, optional): _description_. ID of a user.

        Returns:
            str: _description_
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Gets a userID for a sessionID

        Args:
            session_id (str, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """returns a User instance based on a cookie value"""
        cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(os.getenv('SESSION_NAME'))

        user = User(user_id)

        return user
