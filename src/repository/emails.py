from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Email, User
from src.schemas import EmailModel


async def get_emails(skip: int, limit: int, user: User, db: Session) -> List[Email]:
    """
    Retrieves a list of emails for a specific user with specified pagination parameters.

    :param skip: The number of emails to skip.
    :type skip: int
    :param limit: The maximum number of emails to return.
    :type limit: int
    :param user: The user to retrieve emails for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of emails.
    :rtype: List[Note]
    """
    return db.query(Email).filter(Email.user_id == user.id).offset(skip).limit(limit).all()


async def get_email(email_id: int, user: User, db: Session) -> Email:
    """
       Retrieves a single email with the specified ID for a specific user.

       :param email_id: The ID of the email to retrieve.
       :type email_id: int
       :param user: The user to retrieve the email for.
       :type user: User
       :param db: The database session.
       :type db: Session
       :return: The email with the specified ID, or None if it does not exist.
       :rtype: Note | None
       """
    return db.query(Email).filter(and_(Email.id == email_id, Email.user_id == user.id)).first()


async def create_email(body: EmailModel, user: User, db: Session) -> Email:
    """
        Creates a new email for a specific user.

        :param body: The data for the email to create.
        :type body: EmailModel
        :param user: The user to create the email for.
        :type user: User
        :param db: The database session.
        :type db: Session
        :return: The newly created email.
        :rtype: Note
        """
    email = Email(email=body.email, user_id=user.id)
    db.add(email)
    db.commit()
    db.refresh(email)
    return email


async def update_email(email_id: int, body: EmailModel, user: User, db: Session) -> Email | None:
    """
       Updates a single email with the specified ID for a specific user.

       :param email_id: The ID of the email to update.
       :type email_id: int
       :param body: The updated data for the email.
       :type body: EmailModel
       :param user: The user to update the email for.
       :type user: User
       :param db: The database session.
       :type db: Session
       :return: The updated email, or None if it does not exist.
       :rtype: Note | None
       """
    email = db.query(Email).filter(and_(Email.id == email_id, Email.user_id == user.id)).first()
    if email:
        email.email = body.email
        db.commit()
    return email


async def remove_email(email_id: int, user: User, db: Session)  -> Email | None:
    """
        Removes a single email with the specified ID for a specific user.

        :param email_id: The ID of the email to remove.
        :type email_id: int
        :param user: The user to remove the email for.
        :type user: User
        :param db: The database session.
        :type db: Session
        :return: The removed email, or None if it does not exist.
        :rtype: Note | None
        """
    email = db.query(Email).filter(and_(Email.id == email_id, Email.user_id == user.id)).first()
    if email:
        db.delete(email)
        db.commit()
    return email
