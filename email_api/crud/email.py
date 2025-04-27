from sqlalchemy.orm import Session

from schemas.email import EmailCreate
from models.email import Email


def crear_email(db: Session, email: EmailCreate):
    db_email = Email(
        to_address=email.to_address,
        cc_address=email.cc_address,
        bcc_address=email.bcc_address,
        subject=email.subject,
        body_html=email.body_html,
        template_id=email.template_id,
    )
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    return db_email

def correos_pendientes(db: Session, limit: int = 5):
    return db.query(Email).filter(Email.status == "pendiente").limit(limit).all()

def actualizar_estado(db: Session, email_id: int, status: str):
    db_email = db.query(Email).filter(Email.id == email_id).first()
    if db_email:
        db_email.status = status
        if status == "enviado":
            from datetime import datetime
            db_email.sent_at = datetime.utcnow()
        db.commit()
        db.refresh(db_email)
    return db_email
