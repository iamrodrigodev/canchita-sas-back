from pydantic import BaseModel, Field
from app.modules.empresas.schemas.validaciones import EmpresaValidacionConstantes

class EmpresaGestionActualizarPeticion(BaseModel):
    nombre_comercial: str = Field(..., max_length=EmpresaValidacionConstantes.NOMBRE_COMERCIAL_MAX)
    razon_social: str | None = Field(None, max_length=EmpresaValidacionConstantes.RAZON_SOCIAL_MAX)
    ruc: str | None = Field(None, max_length=EmpresaValidacionConstantes.RUC_MAX)
    subdominio: str = Field(..., max_length=EmpresaValidacionConstantes.SUBDOMINIO_MAX)

class EmpresaGestionEstadoPeticion(BaseModel):
    estado: int = Field(..., description="1: Activo, 0: Inactivo, 2: Suspendido")
