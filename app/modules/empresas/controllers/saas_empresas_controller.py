from fastapi import APIRouter, Depends
from app.core.responses.api_respuesta import ApiDeRespuesta
from app.core.responses.mensajes_confirmacion import MensajesDeConfirmacion
from app.core.security.seguridad import requiere_rol, obtener_usuario_actual_id
from app.modules.usuarios.enums.roles_sistema import RolesSistema
from app.modules.empresas.schemas.peticion.empresa_crear_peticion import EmpresaCrearPeticion
from app.modules.empresas.services.empresa_service import IEmpresaService
from app.modules.empresas.services.impl.empresa_service_impl import get_empresa_service

saas_empresas_router = APIRouter()

@saas_empresas_router.post('', dependencies=[Depends(requiere_rol(RolesSistema.SUPER_ADMIN.value))])
async def crear_empresa_saas(
    peticion: EmpresaCrearPeticion,
    saas_admin_id: int = Depends(obtener_usuario_actual_id),
    servicio: IEmpresaService = Depends(get_empresa_service)
):
    """
    Endpoint exclusivo para SUPER_ADMIN.
    Permite registrar una nueva empresa y vincularla a un USUARIO_COMUN como su ADMIN_EMPRESA.
    """
    respuesta = await servicio.crear_empresa(peticion, saas_admin_id)
    return ApiDeRespuesta.creado("Empresa creada y asignada exitosamente", respuesta.model_dump())
