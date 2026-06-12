from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EmpresaRespuesta(BaseModel):
    id: int
    nombre_comercial: str
    razon_social: Optional[str]
    ruc: Optional[str]
    subdominio: str
    estado: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True
