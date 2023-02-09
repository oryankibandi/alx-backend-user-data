#!/usr/bin/env python3

from api.v1.auth.auth import Auth
from models.user import User
import base64
import binascii
import typing


class BasicAuth(Auth):
    """Basic auth class.
    Inherits from Auth class

    Args:
        Auth (_type_): _description_
    """

    def __init__(self):
        """Initialized a BasicAuth instance
        """
        super().__init__()

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extracts base64 part of the authorization
        header

        Args:
            authorization_header (str): header

        Returns:
            str: base64 part of the header
        """

        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if authorization_header.split(' ')[0] != 'Basic':
            return None

        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decodes a base64 auth header

        Args:
            base64_authorization_header (str): base64 header

        Returns:
            str: decoded string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded = base64.b64decode(
                bytes(base64_authorization_header, 'utf-8'))
            return decoded.decode('utf-8')
        except binascii.Error:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
    ) -> typing.Tuple(str, str):
        """Extracts username and password from a decoded
        base64 string

        Args:
            str (decoded_base64_authorization_header): Decoded header
        """

        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return None
        if ':' not in decoded_base64_authorization_header:
            return None

        credentials = decoded_base64_authorization_header.split(':')
        email = credentials[0]
        password = credentials[1]

        if len(credentials) > 2:
            pass_list = credentials[2:]
            password = ':'.join(pass_list)

        return (email, password)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> typing.TypeVar('User'):
        """Retrieves user from credentials"""
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        n_user = User({'email': user_email, '_password': user_pwd})

        users = n_user.search({'email': user_email})
        if users is None:
            return None

        if not n_user.is_valid_password(users[0]._password):
            return None

        return users[0]

    def current_user(self, request=None) -> typing.TypeVar('User'):
        """retrieves the User instance"""
        auth_header = self.authorization_header(request)
        base64_header = self.extract_base64_authorization_header(auth_header)
        decoded_header = self.decode_base64_authorization_header(base64_header)
        user_cred = self.extract_user_credentials(decoded_header)
        user = self.user_object_from_credentials(user_cred[0], user_cred[1])

        return user
