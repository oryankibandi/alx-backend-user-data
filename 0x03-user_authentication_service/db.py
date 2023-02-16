#!/usr/bin/env python3
"""DB Module
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
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
        """Creates an entry of user"""
        new_user = User()
        new_user.email = email
        new_user.hashed_password = hashed_password

        self.__session.add(new_user)
        self.__session.commit()

        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Finds a user"""

        query = self.__session.query(User)

        try:
            for k, v in kwargs.items():
                query = query.filter(getattr(User, k) == v)
                user = query.first()

                if len(user) <= 0:
                    raise NoResultFound
                else:
                    return user
        except:
            raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates a user with the given user_id"""
        user = self.find_user_by(id=user_id)

        try:
            for k, v in kwargs.items():
                setattr(user, k, v)
        except:
            raise ValueError

        self._session.commit()
