from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from database import Base

class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    de = Column(String(255), nullable=False)
    para = Column(String(255), nullable=False)
    concopia = Column(Text, nullable=True)
    concopiaoculta = Column(Text, nullable=True)
    asunto = Column(String(255), nullable=True)
    parametros = Column(Text, nullable=False)
    cuerpoHtml = Column(Text, nullable=True)
    status = Column(String(20), default="pending")
    error = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
