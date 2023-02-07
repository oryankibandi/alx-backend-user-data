#!/usr/bin/env python3
from typing import List, TypeVar
from flask import request


class Auth:
    """Auth class template"""

    def __init__(self):
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """_summary_

        Args:
            path (str): _description_
            excluded_paths (List[str]): _description_

        Returns:
            bool: _description_
        """
        if excluded_paths is None or path is None:
            return True

        if path[-1] is not '/':
            path = path + '/'

        if excluded_paths.count(path) <= 0:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """Retrieves the auth header

        Args:
            request (_type_, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        if request is None:
            return None
        if request.headers.get('Authorization') is None:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Gets the current user
        """
        return None
