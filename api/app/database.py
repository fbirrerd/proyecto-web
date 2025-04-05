from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Puedes usar dotenv para manejar las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/mi_basedatos")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
