from sqlalchemy import Column, String, SmallInteger
from app.db.sesion import Base
from app.modules.empresas.schemas.validaciones import RolEmpresaValidacionConstantes

class RolEmpresa(Base):
    __tablename__ = 'roles_empresa'
    __table_args__ = {'schema': 'empresas'}

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    nombre = Column(String(RolEmpresaValidacionConstantes.NOMBRE_ROL_MAX), nullable=False, unique=True)

    def __repr__(self):
        return f'<RolEmpresa {self.nombre}>'
