from sqlalchemy.orm import Session
from models.email import Email
from schemas.email import EmailCreate

def crear_email(db: Session, email: EmailCreate):
    db_email = Email(**email.dict())
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    return db_email

def obtener_email(db: Session, email_id: int):
    return db.query(Email).filter(Email.id == email_id).first()

def obtener_emails(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Email).offset(skip).limit(limit).all()