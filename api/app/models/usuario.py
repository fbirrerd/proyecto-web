# app/models/usuario.py
from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    direccion_id = Column(Integer, ForeignKey("direcciones.id"), nullable=True)
    fecha_creacion = Column(TIMESTAMP, default="CURRENT_TIMESTAMP")
    fecha_modificacion = Column(TIMESTAMP, default="CURRENT_TIMESTAMP")
    estado = Column(SmallInteger, default=0)  # 0: Habilitado, 1: Deshabilitado
    duracion = Column(Integer, default=20)  # Duración de sesión

    # Relación con la tabla de direcciones
    direccion = relationship("Direccion", back_populates="usuarios")
