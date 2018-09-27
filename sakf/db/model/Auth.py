# -*- coding: utf-8 -*-
import sqlalchemy
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AuthGroup(Base):
    __tablename__ = 'auth_group'

    id = sqlalchemy.Column(INTEGER(11), primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(50), nullable=False)
    url_route = sqlalchemy.Column(sqlalchemy.Text)


class AuthUrl(Base):
    __tablename__ = 'auth_url'

    id = sqlalchemy.Column(INTEGER(11), primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    url = sqlalchemy.Column(sqlalchemy.Text)


class AuthUser(Base):
    __tablename__ = 'auth_user'

    id = sqlalchemy.Column(INTEGER(11), primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(50), nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    super = sqlalchemy.Column(TINYINT(4), nullable=False, server_default=sqlalchemy.text("0"))
    lock = sqlalchemy.Column(TINYINT(4), nullable=False, server_default=sqlalchemy.text("0"))
    group_id = sqlalchemy.Column(sqlalchemy.ForeignKey('auth_group.id'), nullable=False, index=True)
    ctime = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, server_default=sqlalchemy.text("current_timestamp() ON UPDATE current_timestamp()"))
    ltime = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, server_default=sqlalchemy.text("current_timestamp() ON UPDATE current_timestamp()"))

    group = relationship('AuthGroup')
