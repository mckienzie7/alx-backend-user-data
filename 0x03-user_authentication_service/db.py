#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User  # Added import for User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
            - Update user based on it's user_id
        """
        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            self._session.commit()
        except NoResultFound:
            raise ValueError(f"No user found with id {user_id}")
        except MultipleResuktFound:
            raise ValueError(f"Multiple user found with id {user_id}")

        return None

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
