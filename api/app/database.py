import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Leer la URL de conexión desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

# Validación básica de la URL de la base de datos
if not DATABASE_URL:
    raise ValueError("La variable de entorno DATABASE_URL no está definida")

# Crear el motor de conexión a la base de datos
engine = create_engine(DATABASE_URL, echo=False)  # Puedes poner echo=True para debug

# Crear una sesión local para interactuar con la base de datos
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Base para modelos ORM
Base = declarative_base()

def init_db():
    """
    Inicializa la base de datos creando todas las tablas definidas en los modelos ORM.
    """
    Base.metadata.create_all(bind=engine)

# Dependencia para usar en rutas con FastAPI
def get_db():
    """
    Genera una sesión de base de datos y la cierra automáticamente.
    Uso:
        db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
