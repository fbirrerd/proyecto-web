from sqlalchemy import Column, Integer, ForeignKey, Date, TIMESTAMP, PrimaryKeyConstraint
from app.database import Base
from sqlalchemy.sql import func

class UsuarioEmpresa(Base):
    __tablename__ = "usuario_empresa"

    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    empresa_id = Column(Integer, ForeignKey("empresa.id"), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())
    fecha_modificacion = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        PrimaryKeyConstraint('usuario_id', 'empresa_id'),
    )
