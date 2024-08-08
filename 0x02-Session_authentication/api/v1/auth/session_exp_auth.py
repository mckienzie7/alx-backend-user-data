#!/usr/bin/env python3
"""Session authentication with expiration date"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class"""
    def __init__(self):
        """Init class"""
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """overload create_session function from SessiionAuth"""
        try:
            session_id = super().create_session(user_id)

        except Exception:
            return None

        if session_id is None:
            return None

        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """return id based on session id"""
        if session_id is None:
            return None

        if session_id not in self.user_id_by_session_id.keys():
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if self.session_duration <= 0:
            return session_dict.get('user_id')

        created_at = session_dict.get('created_at')
        if created_at is None:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)

        if expiration_time < datetime.now():
            return None

        return session_dict.get('user_id')
