from sqlalchemy import Column, Integer, SmallInteger, String, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.id"), nullable=True)

    nombre = Column(String(255), nullable=False)
    tipo = Column(String(10), nullable=False)
    url = Column(String(255), nullable=False)
    icono = Column(String(50), nullable=True)
    orden = Column(Integer, nullable=True)

    padre_id = Column(Integer, ForeignKey("menu.id", ondelete="SET NULL"), nullable=True)

    fecha_creacion = Column(TIMESTAMP, server_default=func.now())
    fecha_modificacion = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    estado = Column(SmallInteger, default=0)

    # Relaciones
    hijos = relationship("Menu", backref="padre", remote_side=[id])
