from fastapi import APIRouter, Depends, Query

from app.core.dependencies.dependencias import get_usuario_service
from app.core.responses.api_respuesta import ApiDeRespuesta
from app.core.responses.mensajes_confirmacion import MensajesDeConfirmacion
from app.core.security.seguridad import (
    obtener_usuario_actual,
    obtener_usuario_actual_id,
    requiere_rol,
    verificar_propietario_o_admin,
)
from app.modules.usuarios.schemas.esquemas_usuario_gestion_peticion import (
    UsuarioGestionActualizarPeticion,
    UsuarioGestionCrearPeticion,
    UsuarioGestionEstadoPeticion,
)
from app.modules.usuarios.services.usuario_service import IUsuarioService

usuario_router = APIRouter()
usuarios_gestion_router = APIRouter()


@usuario_router.get('/perfil')
async def obtener_mi_perfil(
    usuario_actual=Depends(obtener_usuario_actual),
    servicio_usuario: IUsuarioService = Depends(get_usuario_service)
):
    respuesta = await servicio_usuario.obtener_perfil(usuario_actual)
    return ApiDeRespuesta.exito(MensajesDeConfirmacion.DATOS_OBTENIDOS, respuesta.model_dump())


@usuario_router.get('/{usuario_id}/perfil')
async def obtener_perfil_por_usuario_id(
    usuario_id: int,
    usuario_actual=Depends(obtener_usuario_actual),
    servicio_usuario: IUsuarioService = Depends(get_usuario_service)
):
    verificar_propietario_o_admin(usuario_id, usuario_actual)
    respuesta = await servicio_usuario.obtener_perfil_por_id(usuario_id)
    return ApiDeRespuesta.exito(MensajesDeConfirmacion.DATOS_OBTENIDOS, respuesta.model_dump())


@usuarios_gestion_router.post('')
async def crear_usuario_gestion(
    peticion: UsuarioGestionCrearPeticion,
    _admin=Depends(requiere_rol("ADMINISTRADOR")),
    administrador_id: int = Depends(obtener_usuario_actual_id),
    servicio_usuario: IUsuarioService = Depends(get_usuario_service),
):
    respuesta = await servicio_usuario.crear_usuario_gestion(peticion, administrador_id)
    return ApiDeRespuesta.creado('Usuario creado correctamente', respuesta.model_dump())


@usuarios_gestion_router.get('')
async def listar_usuarios_gestion(
    pagina: int = Query(default=1),
    tamano: int = Query(default=10),
    correo: str | None = Query(default=None),
    rol: int | None = Query(default=None),
    estado: int | None = Query(default=None),
    _admin=Depends(requiere_rol("ADMINISTRADOR")),
    servicio_usuario: IUsuarioService = Depends(get_usuario_service),
):
    respuesta = await servicio_usuario.listar_usuarios_gestion(pagina, tamano, correo, rol, estado)
    return ApiDeRespuesta.exito(MensajesDeConfirmacion.DATOS_OBTENIDOS, respuesta.model_dump())


@usuarios_gestion_router.get('/{usuario_id}')
async def obtener_usuario_gestion(
    usuario_id: int,
    _admin=Depends(requiere_rol("ADMINISTRADOR")),
    servicio_usuario: IUsuarioService = Depends(get_usuario_service),
):
    respuesta = await servicio_usuario.obtener_usuario_gestion(usuario_id)
    return ApiDeRespuesta.exito(MensajesDeConfirmacion.DATOS_OBTENIDOS, respuesta.model_dump())


@usuarios_gestion_router.put('/{usuario_id}')
async def actualizar_usuario_gestion(
    usuario_id: int,
    peticion: UsuarioGestionActualizarPeticion,
    _admin=Depends(requiere_rol("ADMINISTRADOR")),
    administrador_id: int = Depends(obtener_usuario_actual_id),
    servicio_usuario: IUsuarioService = Depends(get_usuario_service),
):
    respuesta = await servicio_usuario.actualizar_usuario_gestion(usuario_id, peticion, administrador_id)
    return ApiDeRespuesta.exito('Usuario actualizado correctamente', respuesta.model_dump())


@usuarios_gestion_router.patch('/{usuario_id}/estado')
async def cambiar_estado_usuario_gestion(
    usuario_id: int,
    peticion: UsuarioGestionEstadoPeticion,
    _admin=Depends(requiere_rol("ADMINISTRADOR")),
    administrador_id: int = Depends(obtener_usuario_actual_id),
    servicio_usuario: IUsuarioService = Depends(get_usuario_service),
):
    respuesta = await servicio_usuario.cambiar_estado_usuario_gestion(usuario_id, peticion.estado, administrador_id)
    return ApiDeRespuesta.exito('Estado actualizado correctamente', respuesta.model_dump())


@usuarios_gestion_router.delete('/{usuario_id}')
async def eliminar_logico_usuario_gestion(
    usuario_id: int,
    _admin=Depends(requiere_rol("ADMINISTRADOR")),
    administrador_id: int = Depends(obtener_usuario_actual_id),
    servicio_usuario: IUsuarioService = Depends(get_usuario_service),
):
    await servicio_usuario.eliminar_logico_usuario_gestion(usuario_id, administrador_id)
    return ApiDeRespuesta.exito('Usuario desactivado correctamente')
