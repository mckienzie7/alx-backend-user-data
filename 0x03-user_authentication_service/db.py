#!/usr/bin/env python3
"""User Database Module."""

from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """Class for managing user data in the database."""

    def __init__(self) -> None:
        """Initialize a new UserDB instance."""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Get the database session."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Create a new user in the database."""
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **filters) -> User:
        """Find a user in the database based on filters."""
        filter_fields, filter_values = [], []
        for field, value in filters.items():
            if hasattr(User, field):
                filter_fields.append(getattr(User, field))
                filter_values.append(value)
            else:
                raise InvalidRequestError(f"Invalid filter: {field}")
        user = self._session.query(User).filter(
            tuple_(*filter_fields).in_([tuple(filter_values)])
        ).first()
        if user is None:
            raise NoResultFound("User not found.")
        return user

    def update_user(self, user_id: int, **updates) -> None:
        """Update user information in the database."""
        user = self.find_user_by(id=user_id)
        if user is None:
            return
        update_fields = {}
        for key, value in updates.items():
            if hasattr(User, key):
                update_fields[getattr(User, key)] = value
            else:
                raise ValueError(f"Invalid field: {key}")
        self._session.query(User).filter(User.id == user_id).update(
            update_fields,
            synchronize_session=False,
        )
        self._session.commit()
