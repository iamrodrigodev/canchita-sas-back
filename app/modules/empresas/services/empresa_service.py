from abc import ABC, abstractmethod
from app.modules.empresas.schemas.peticion.empresa_crear_peticion import EmpresaCrearPeticion
from app.modules.empresas.schemas.peticion.empresa_gestion_peticion import EmpresaGestionActualizarPeticion
from app.modules.empresas.schemas.respuesta.empresa_respuesta import EmpresaRespuesta
from app.modules.empresas.schemas.respuesta.empresa_paginacion_respuesta import EmpresaPaginacionRespuesta

class IEmpresaService(ABC):
    @abstractmethod
    async def crear_empresa(self, peticion: EmpresaCrearPeticion, saas_admin_id: int) -> EmpresaRespuesta:
        pass

    @abstractmethod
    async def listar_empresas(self, pagina: int, tamano: int, busqueda: str | None, estado: int | None) -> EmpresaPaginacionRespuesta:
        pass

    @abstractmethod
    async def obtener_empresa(self, empresa_id: int) -> EmpresaRespuesta:
        pass

    @abstractmethod
    async def actualizar_empresa(self, empresa_id: int, peticion: EmpresaGestionActualizarPeticion, saas_admin_id: int) -> EmpresaRespuesta:
        pass

    @abstractmethod
    async def cambiar_estado_empresa(self, empresa_id: int, estado: int, saas_admin_id: int) -> EmpresaRespuesta:
        pass
