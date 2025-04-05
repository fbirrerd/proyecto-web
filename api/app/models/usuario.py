from sqlalchemy import Column, Integer, String, TIMESTAMP, SmallInteger
from app.database import Base
from sqlalchemy.sql import func

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    contrasena = Column(String(255), nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())
    fecha_modificacion = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    estado = Column(SmallInteger, default=0)
    duracion = Column(Integer, default=20)
