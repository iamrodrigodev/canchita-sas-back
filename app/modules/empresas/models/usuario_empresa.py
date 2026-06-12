from sqlalchemy import Column, BigInteger, SmallInteger, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.db.sesion import Base
from app.utils.tiempo_util import TiempoUtil

class UsuarioEmpresa(Base):
    __tablename__ = 'usuarios_empresas'
    __table_args__ = (
        Index('ix_usuarios_empresas_usuario', 'usuario_id'),
        Index('ix_usuarios_empresas_empresa_rol', 'empresa_id', 'rol_empresa_id'),
        {'schema': 'empresas'}
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    usuario_id = Column(BigInteger, ForeignKey('autenticacion.usuarios.id'), nullable=False)
    empresa_id = Column(BigInteger, ForeignKey('empresas.empresas.id'), nullable=False)
    rol_empresa_id = Column(SmallInteger, ForeignKey('empresas.roles_empresa.id'), nullable=False)
    
    estado = Column(SmallInteger, default=1)  # 1: Activo, 0: Inactivo
    
    fecha_asignacion = Column(DateTime, default=lambda: TiempoUtil.ahora_utc_sin_tz())

    # Relaciones
    usuario = relationship('Usuario', back_populates='empresas_asignadas')
    empresa = relationship('Empresa', back_populates='usuarios_empresa')
    rol_empresa = relationship('RolEmpresa')

    def __repr__(self):
        return f'<UsuarioEmpresa U:{self.usuario_id} E:{self.empresa_id}>'
