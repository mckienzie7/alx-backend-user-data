#!/usr/bin/env python3
"""A class that inherits from Auth class"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from typing import List, TypeVar
from models.user import User


class BasicAuth(Auth):
    """Inherits from Auth"""
    def extract_base64_authorization_header(
        self,
        authorization_header: str
    ) -> str:
        """hat returns the Base64 part of
        the Authorization header for a Basic Authentication
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(
        self,
        base64_authorization_header: str
    ) -> str:
        """Return decoded data of base64"""

        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded64 = b64decode(base64_authorization_header)
            decoded = decoded64.decode('utf-8')
        except Exception:
            return None

        return decoded

    def extract_user_credentials(
        self,
        decoded_base64_authorization_header: str
    ) -> (str, str):
        """return email and from base64 decoded value"""

        if decoded_base64_authorization_header is None:
            return (None, None)

        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)

        if ":" not in decoded_base64_authorization_header:
            return (None, None)

        list_items = decoded_base64_authorization_header.split(":", 1)

        return (list_items[0], list_items[1])

    def user_object_from_credentials(
        self,
        user_email: str,
        user_pwd: str
    ) -> TypeVar('User'):
        """return user that matches password and email"""
        if user_email is None or user_pwd is None:
            return None

        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None

        try:
            users: List['User'] = User.search({"email": user_email})

        except Exception:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Using all the authentications return user"""
        auth_header: str = self.authorization_header(request)

        if not auth_header:
            return None

        extract_auth_header: str = self.extract_base64_authorization_header(
            auth_header
        )

        if not extract_auth_header:
            return None

        decoded_auth_header: str = self.decode_base64_authorization_header(
            extract_auth_header
        )

        if not decoded_auth_header:
            return None

        user_credentials: (str, str) = self.extract_user_credentials(
            decoded_auth_header
        )

        if user_credentials[0] is None and user_credentials[1] is None:
            return None

        user = self.user_object_from_credentials(
            user_credentials[0],
            user_credentials[1]
        )

        if not user:
            return None

        return user
