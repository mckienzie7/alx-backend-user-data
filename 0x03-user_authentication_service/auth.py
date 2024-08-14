#!/usr/bin/env python3

from db import DB
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User
import bcrypt
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generates a UUID."""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a user based on email and password.
        Raise ValueError if user with email already exists.
        """
        try:
            # Check if the user already exists
            user1 = self._db.find_user_by(email=email)
        except NoResultFound:
            user = self._db.add_user(email, _hash_password(password))
            return user
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password) -> bool:
        """
            - Validate user's Password
        """
        try:
            user = self._db.find_user_by(email=email)
            if useri:
                encode = password.encode('utf-8')
                if bcrypt.checkpw(encode, user.hashed_password):
                    return True
                return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> Union[str, None]:
        """
            - Create Session id based on email
        """
        try:
            user1 = self._db.find_user_by(email=email)
            if user1:
                session_id = _generate_uuid()
                user1.session_id = session_id
                self._db._session.add(user1)
                self._db._session.commit()
                return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(session_id: str) -> User:
        """
            Get the user from corresponding session id
        """
        if session_id is None:
            return
        user = AUTH._bd.find_user_by(session_id=session_id)
        if not user:
            return

        return user

    def destroy_session(user_id: int) -> None:
        """
            Destroy Session by updatin user session id to None
        """
        if user_id is None:
            return

        user = AUTH._bd.find_user_by(session_id=session_id)
        if not user:
            return

        user.session_id = None
        return None
