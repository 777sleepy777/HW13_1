from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Email, User
from src.schemas import EmailModel


async def get_emails(skip: int, limit: int, user: User, db: Session) -> List[Email]:
    return db.query(Email).filter(Email.user_id == user.id).offset(skip).limit(limit).all()


async def get_email(email_id: int, user: User, db: Session) -> Email:
    return db.query(Email).filter(and_(Email.id == email_id, Email.user_id == user.id)).first()


async def create_email(body: EmailModel, user: User, db: Session) -> Email:
    email = Email(email=body.email, user_id=user.id)
    db.add(email)
    db.commit()
    db.refresh(email)
    return email


async def update_email(email_id: int, body: EmailModel, user: User, db: Session) -> Email | None:
    email = db.query(Email).filter(and_(Email.id == email_id, Email.user_id == user.id)).first()
    if email:
        email.email = body.email
        db.commit()
    return email


async def remove_email(email_id: int, user: User, db: Session)  -> Email | None:
    email = db.query(Email).filter(and_(Email.id == email_id, Email.user_id == user.id)).first()
    if email:
        db.delete(email)
        db.commit()
    return email
