from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    to_address = Column(String, nullable=False)
    cc_address = Column(String, nullable=True)
    bcc_address = Column(String, nullable=True)
    subject = Column(String, nullable=False)
    body_html = Column(Text, nullable=False)
    status = Column(String, default="pendiente")
    template_id = Column(Integer, ForeignKey("templates.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime, nullable=True)

    template = relationship("Template")
