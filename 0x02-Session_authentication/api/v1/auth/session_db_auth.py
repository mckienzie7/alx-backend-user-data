#!/usr/bin/env python3
""""saving the session id and user id to a database like a file"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Class inherts from SessionExPAuth and also saves the data to file db
    """
    def create_session(self, user_id=None):
        """
        Override the create_session base class and save session to database"""
        try:
            session_id = super().create_session(user_id)
        except Exception:
            return None

        if session_id is None:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)

        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Get user id depending on session_id"""
        if session_id is None:
            return None

        UserSession.load_from_file()
        sessions = UserSession.search({
            'session_id': session_id
        })

        if not sessions:
            return None

        session = sessions[0]

        expired_time = session.created_at + \
            timedelta(seconds=self.session_duration)

        if expired_time < datetime.utcnow():
            return None

        return session.user_id

    def destroy_session(self, request=None):
        """delete user session from database"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)

        if not user_id:
            return False

        sessions = UserSession.search({
            'session_id': session_id
        })

        if not sessions:
            return False

        session = sessions[0]

        try:
            session.remove()
            UserSession.save_to_file()
        except Exception:
            return False

        return True
