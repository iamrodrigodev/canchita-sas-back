from pydantic import BaseModel, Field, EmailStr
from app.modules.empresas.schemas.validaciones import EmpresaValidacionConstantes

class EmpresaCrearPeticion(BaseModel):
    nombre_comercial: str = Field(..., max_length=EmpresaValidacionConstantes.NOMBRE_COMERCIAL_MAX)
    razon_social: str | None = Field(None, max_length=EmpresaValidacionConstantes.RAZON_SOCIAL_MAX)
    ruc: str | None = Field(None, max_length=EmpresaValidacionConstantes.RUC_MAX)
    subdominio: str = Field(..., max_length=EmpresaValidacionConstantes.SUBDOMINIO_MAX)
    
    # Usuario a vincular como dueño
    usuario_dueño_id: int = Field(..., description="ID del usuario que será asignado como ADMIN_EMPRESA")
