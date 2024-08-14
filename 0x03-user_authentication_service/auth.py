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
            if user:
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
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if user is None:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """
            Get the user from corresponding session id
        """
        user = None
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """
            Destroy Session by updatin user session id to None
        """
        if user_id is None:
            return

        user = self._db.update_user(user_id, session_id=None)

    def get_reset_password(email: str) -> str:
        """
            Reset Password
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError("User not found")

        rt_id = _generate_uuid()
        self._db.update_user(user.id, reset_token=rt_id)
        return rt_id

    def update_passsword(reset_token: str, password: str) -> None:
        """
            Update Password
        """
        user = None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError("Invalid reset token")
        new_password = _hash_password(password)
        self._db.update_user(
                user.id,
                hashed_password=new_password,
                reset_token=None
                )
