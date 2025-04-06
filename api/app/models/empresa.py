import os
from sqlalchemy import create_engine, Column, Integer, String, SmallInteger, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime


Base = declarative_base()

class Empresa(Base):
    __tablename__ = 'empresa'
    
    # Definición de las columnas
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False, unique=True)
    fecha_creacion = Column(TIMESTAMP, default=datetime.utcnow)
    fecha_modificacion = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    estado = Column(SmallInteger, nullable=False, default=0)  # 0: Habilitado, 1: Deshabilitado

