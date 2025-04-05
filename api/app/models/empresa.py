from sqlalchemy import Column, Integer, String, TIMESTAMP, SmallInteger
from app.database import Base
from sqlalchemy.sql import func

class Empresa(Base):
    __tablename__ = "empresa"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), unique=True, nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())
    fecha_modificacion = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    estado = Column(SmallInteger, default=0)
