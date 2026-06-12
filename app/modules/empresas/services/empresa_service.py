from abc import ABC, abstractmethod
from app.modules.empresas.schemas.peticion.empresa_crear_peticion import EmpresaCrearPeticion
from app.modules.empresas.schemas.respuesta.empresa_respuesta import EmpresaRespuesta

class IEmpresaService(ABC):
    @abstractmethod
    async def crear_empresa(self, peticion: EmpresaCrearPeticion, saas_admin_id: int) -> EmpresaRespuesta:
        pass
