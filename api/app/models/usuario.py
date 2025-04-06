import os
from sqlalchemy import create_engine, Column, Integer, String, SmallInteger, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.sql import func


Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'

    # Definición de las columnas
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_usuario = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    contrasena = Column(String(255), nullable=False)  # Considera usar hashing para contraseñas
    fecha_creacion = Column(TIMESTAMP, default=datetime.utcnow)
    fecha_modificacion = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    estado = Column(SmallInteger, nullable=False, default=0)  # 0: Habilitado, 1: Deshabilitado
    duracion = Column(Integer, default=20)  # Duración con valor por defecto de 20
