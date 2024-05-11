from sqlalchemy import Column, Integer, String, Date, Boolean, UniqueConstraint, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(100))
    birthday = Date
    description = Column(String(250))
    email_id = Column(Integer, ForeignKey("emails.id"), nullable=True)
    emails = relationship("Email", backref="contacts")
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="contacts")



class Email(Base):
    __tablename__ = "emails"
    __table_args__ = (
        UniqueConstraint('email', 'user_id', name='unique_email_user'),
    )
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True, nullable=False)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="emails")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    confirmed = Column(Boolean, default=False)
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)

