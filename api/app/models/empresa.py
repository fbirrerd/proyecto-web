import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, SmallInteger, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Cargar variables de entorno desde el archivo .env
load_dotenv()

Base = declarative_base()

class Empresa(Base):
    __tablename__ = 'empresa'
    
    # Definición de las columnas
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False, unique=True)
    fecha_creacion = Column(TIMESTAMP, default=datetime.utcnow)
    fecha_modificacion = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    estado = Column(SmallInteger, nullable=False, default=0)  # 0: Habilitado, 1: Deshabilitado

# Obtener información de la base de datos desde las variables de entorno
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# Construir la URL de la base de datos
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Configuración de la base de datos
engine = create_engine(DATABASE_URL, echo=True)

# Crear todas las tablas en la base de datos (si no existen ya)
Base.metadata.create_all(bind=engine)

# Crear la sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener una sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
