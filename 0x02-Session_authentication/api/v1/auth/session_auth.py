#!/usr/bin/env python3
"""
    - SessionAuth creation
"""
from api.v1.auth.auth import Auth
import os
import uuid


class SessionAuth(Auth):
    """
        - Session!uth class
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:

        if user_id is None and not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:

        if session_id is None and not isinstance(session_id, str):
            return None

        user_id = self.user_id_by_session_id.get(session_id)

        return user_id
