from sqlalchemy import Column, String, BigInteger, SmallInteger, DateTime, Index
from sqlalchemy.orm import relationship
from app.db.sesion import Base
from app.utils.tiempo_util import TiempoUtil
from app.modules.empresas.schemas.validaciones import EmpresaValidacionConstantes

class Empresa(Base):
    __tablename__ = 'empresas'
    __table_args__ = (
        Index('ix_empresas_subdominio', 'subdominio'),
        {'schema': 'empresas'}
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre_comercial = Column(String(EmpresaValidacionConstantes.NOMBRE_COMERCIAL_MAX), nullable=False)
    razon_social = Column(String(EmpresaValidacionConstantes.RAZON_SOCIAL_MAX), nullable=True)
    ruc = Column(String(EmpresaValidacionConstantes.RUC_MAX), nullable=True, unique=True)
    subdominio = Column(String(EmpresaValidacionConstantes.SUBDOMINIO_MAX), nullable=False, unique=True)
    
    estado = Column(SmallInteger, default=1)  # 1: Activo, 0: Inactivo, 2: Suspendido
    
    fecha_creacion = Column(DateTime, default=lambda: TiempoUtil.ahora_utc_sin_tz())
    fecha_actualizacion = Column(
        DateTime,
        default=lambda: TiempoUtil.ahora_utc_sin_tz(),
        onupdate=lambda: TiempoUtil.ahora_utc_sin_tz()
    )

    usuarios_empresa = relationship('UsuarioEmpresa', back_populates='empresa', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Empresa {self.nombre_comercial}>'
