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

from fastapi import Query
from app.core.config.sistema_constantes import SistemaConstantes
from app.modules.empresas.schemas.peticion.empresa_gestion_peticion import EmpresaGestionActualizarPeticion, EmpresaGestionEstadoPeticion

@saas_empresas_router.get('', dependencies=[Depends(requiere_rol(RolesSistema.SUPER_ADMIN.value))])
async def listar_empresas_saas(
    pagina: int = Query(default=SistemaConstantes.PAGINACION_PAGINA_DEFECTO),
    tamano: int = Query(default=SistemaConstantes.PAGINACION_TAMANO_DEFECTO),
    busqueda: str | None = Query(default=None),
    estado: int | None = Query(default=None),
    servicio: IEmpresaService = Depends(get_empresa_service)
):
    respuesta = await servicio.listar_empresas(pagina, tamano, busqueda, estado)
    return ApiDeRespuesta.exito(MensajesDeConfirmacion.DATOS_OBTENIDOS, respuesta.model_dump())

@saas_empresas_router.get('/{empresa_id}', dependencies=[Depends(requiere_rol(RolesSistema.SUPER_ADMIN.value))])
async def obtener_empresa_saas(
    empresa_id: int,
    servicio: IEmpresaService = Depends(get_empresa_service)
):
    respuesta = await servicio.obtener_empresa(empresa_id)
    return ApiDeRespuesta.exito(MensajesDeConfirmacion.DATOS_OBTENIDOS, respuesta.model_dump())

@saas_empresas_router.put('/{empresa_id}', dependencies=[Depends(requiere_rol(RolesSistema.SUPER_ADMIN.value))])
async def actualizar_empresa_saas(
    empresa_id: int,
    peticion: EmpresaGestionActualizarPeticion,
    saas_admin_id: int = Depends(obtener_usuario_actual_id),
    servicio: IEmpresaService = Depends(get_empresa_service)
):
    respuesta = await servicio.actualizar_empresa(empresa_id, peticion, saas_admin_id)
    return ApiDeRespuesta.exito("Empresa actualizada exitosamente", respuesta.model_dump())

@saas_empresas_router.patch('/{empresa_id}/estado', dependencies=[Depends(requiere_rol(RolesSistema.SUPER_ADMIN.value))])
async def cambiar_estado_empresa_saas(
    empresa_id: int,
    peticion: EmpresaGestionEstadoPeticion,
    saas_admin_id: int = Depends(obtener_usuario_actual_id),
    servicio: IEmpresaService = Depends(get_empresa_service)
):
    respuesta = await servicio.cambiar_estado_empresa(empresa_id, peticion.estado, saas_admin_id)
    return ApiDeRespuesta.exito("Estado de empresa actualizado", respuesta.model_dump())
