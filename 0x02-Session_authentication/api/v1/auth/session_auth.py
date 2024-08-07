from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:

        if user_id is None:
            return None

        if not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())

        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(Self, session_id:str = None) -> str:

        if session_id is None:
            return None

        if not isinstance(session_id, str):
            return None

        return Self.user_id_by_session_id.get(session_id)


    def current_user(self, request=None):

        """return user based on session id and user_id"""
        session_id = self.session_cookie(request)

        if session_id is not None:
            user_id = self.user_id_for_session_id(session_id)
            if user_id is not None:

                user = User.get(user_id)

                return user

            return None

        return None
