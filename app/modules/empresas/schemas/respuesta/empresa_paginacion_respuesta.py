from pydantic import BaseModel
from typing import List
from app.modules.empresas.schemas.respuesta.empresa_respuesta import EmpresaRespuesta

class EmpresaPaginacionRespuesta(BaseModel):
    items: List[EmpresaRespuesta]
    total: int
    pagina: int
    tamano: int
