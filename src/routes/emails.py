from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import EmailModel, EmailResponse
from src.repository import emails as repository_emails
from src.services.auth import auth_service

router = APIRouter(prefix='/emails', tags=["emails"])


@router.get("/", response_model=List[EmailResponse])
async def read_emails(db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    emails = await repository_emails.get_emails(current_user, db)
    return emails


@router.get("/{email_id}", response_model=EmailResponse)
async def read_email(email_id: int, db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    email = await repository_emails.get_email(email_id, db)
    if email is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")
    return email


@router.post("/", response_model=EmailResponse, status_code=status.HTTP_201_CREATED)
async def create_email(body: EmailModel, db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user)):
    return await repository_emails.create_email(body, current_user, db)


@router.put("/{email_id}", response_model=EmailResponse)
async def update_email(body: EmailModel, email_id: int, db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    email = await repository_emails.update_email(email_id, body, current_user, db)
    if email is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")
    return email


@router.delete("/{email_id}", response_model=EmailResponse)
async def remove_email(email_id: int, db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    email = await repository_emails.remove_email(email_id, current_user, db)
    if email is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")
    return email
