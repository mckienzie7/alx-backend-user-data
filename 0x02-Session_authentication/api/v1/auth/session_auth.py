#!/usr/bin/env python3
"""A classs SessionAuth that inherits from AUTH"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """Session auth class with a class attribute"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a session id for a user"""
        if user_id is None:
            return None

        if not isinstance(user_id, str):
            return None

        session_id: str = str(uuid4())

        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """eturn user id based on session id"""
        if session_id is None:
            return None

        if not isinstance(session_id, str):
            return None

        user_id = self.user_id_by_session_id.get(session_id)

        return user_id

    def current_user(self, request=None):
        """return user """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)

        user1 = User.get(user_id)
        if user1:
            return user1

    def destroy_session(self, request=None):

        """Delete User Session/ logout """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id)

        if not user_id:
            return False

        del self.user_id_by_session_id[session_id]
        return True
