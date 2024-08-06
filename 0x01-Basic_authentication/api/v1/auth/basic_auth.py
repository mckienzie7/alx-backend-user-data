#!/usr/bin/env python3
"""A class that inherits from Auth class"""
from api.v1.auth.auth import Auth
import base64
class BasicAuth(Auth):

    def extract_base64_authorization_header(self, authorization_header : str) -> str:
        
        if authorization_header is None:
            return None

        if not isinstance(authorization_header,  str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_authorization_header : str) -> str:
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header, validate=True)
            decoded_string = decoded_bytes.decode('utf-8')
            return decoded_string
        except (base64.binascii.Error, ValueError):
            return None
