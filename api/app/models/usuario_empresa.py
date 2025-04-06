from sqlalchemy import Column, Integer, Date, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

# Define el modelo UsuarioEmpresa
class UsuarioEmpresa(Base):
    __tablename__ = 'usuario_empresa'

    usuario_id = Column(Integer, ForeignKey('usuario.id', ondelete="CASCADE"), primary_key=True)
    empresa_id = Column(Integer, ForeignKey('empresa.id', ondelete="CASCADE"), primary_key=True)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    fecha_modificacion = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relación con otras tablas (si es necesario)
    usuario = relationship("Usuario", back_populates="empresas")
    empresa = relationship("Empresa", back_populates="usuarios")

    def __repr__(self):
        return f"<UsuarioEmpresa(usuario_id={self.usuario_id}, empresa_id={self.empresa_id}, fecha_inicio={self.fecha_inicio}, fecha_fin={self.fecha_fin})>"