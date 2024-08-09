#!/usr/bin/env python3
"""Class that saves the session id and user_id to database"""
from models.base import Base


class UserSession(Base):
    """
    Class that inherits from base and saves to file database
    """
    def __init__(self, *args: list, **kwargs: dict):
        """initalize class with user_id and session_id variables"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
