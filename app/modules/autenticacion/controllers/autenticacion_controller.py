from fastapi import APIRouter, Depends, Request
from app.modules.autenticacion.schemas.peticion.registro_schema import RegistroPeticion
from app.modules.autenticacion.schemas.peticion.login_schema import LoginPeticion
from app.modules.autenticacion.schemas.peticion.refrescar_token_schema import RefrescarTokenPeticion
from app.modules.autenticacion.schemas.peticion.recuperacion_clave_schema import (
    SolicitarRecuperacionClavePeticion,
    RestablecerClavePeticion,
)
from app.core.responses.api_respuesta import ApiDeRespuesta
from app.core.responses.mensajes_confirmacion import MensajesDeConfirmacion
from app.core.dependencies.dependencias import get_autenticacion_service
from app.modules.autenticacion.services.autenticacion_service import IAutenticacionService
from app.core.security.seguridad import obtener_usuario_actual_id
from app.core.security.rate_limit import validar_rate_limit_login, validar_rate_limit_refresh, validar_rate_limit_recuperacion


autenticacion_router = APIRouter()


@autenticacion_router.post('/registrar-cuenta', status_code=201)
async def registrar_cuenta(
    peticion: RegistroPeticion,
    servicio_auth: IAutenticacionService = Depends(get_autenticacion_service)
):
    respuesta = await servicio_auth.registrar_cuenta(peticion)
    return ApiDeRespuesta.creado(MensajesDeConfirmacion.CUENTA_REGISTRADA, respuesta.model_dump())


@autenticacion_router.post('/iniciar-sesion')
async def iniciar_sesion(
    request: Request,
    peticion: LoginPeticion,
    servicio_auth: IAutenticacionService = Depends(get_autenticacion_service)
):
    validar_rate_limit_login(request, peticion.correo)
    respuesta = await servicio_auth.iniciar_sesion(peticion)
    return ApiDeRespuesta.exito(MensajesDeConfirmacion.LOGIN_EXITOSO, respuesta.model_dump())


@autenticacion_router.post('/refrescar-token')
async def refrescar_token(
    request: Request,
    peticion: RefrescarTokenPeticion,
    servicio_auth: IAutenticacionService = Depends(get_autenticacion_service)
):
    validar_rate_limit_refresh(request, peticion.token_refresco)
    respuesta = await servicio_auth.refrescar_token(peticion)
    return ApiDeRespuesta.exito(MensajesDeConfirmacion.DATOS_OBTENIDOS, respuesta.model_dump())


@autenticacion_router.post('/cerrar-sesion')
async def cerrar_sesion(
    peticion: RefrescarTokenPeticion,
    servicio_auth: IAutenticacionService = Depends(get_autenticacion_service)
):
    await servicio_auth.cerrar_sesion(peticion)
    return ApiDeRespuesta.exito(MensajesDeConfirmacion.SESION_CERRADA)


@autenticacion_router.post('/cerrar-sesion-todos')
async def cerrar_sesion_todos(
    usuario_actual_id: int = Depends(obtener_usuario_actual_id),
    servicio_auth: IAutenticacionService = Depends(get_autenticacion_service)
):
    await servicio_auth.cerrar_sesion_todos(usuario_actual_id)
    return ApiDeRespuesta.exito(MensajesDeConfirmacion.SESION_CERRADA)


@autenticacion_router.post('/solicitar-recuperacion-clave')
async def solicitar_recuperacion_clave(
    request: Request,
    peticion: SolicitarRecuperacionClavePeticion,
    servicio_auth: IAutenticacionService = Depends(get_autenticacion_service)
):
    validar_rate_limit_recuperacion(request, peticion.correo)
    await servicio_auth.solicitar_recuperacion_clave(peticion)
    return ApiDeRespuesta.exito("Si el correo existe, se enviara un enlace de recuperacion")


@autenticacion_router.post('/restablecer-clave')
async def restablecer_clave(
    peticion: RestablecerClavePeticion,
    servicio_auth: IAutenticacionService = Depends(get_autenticacion_service)
):
    await servicio_auth.restablecer_clave(peticion)
    return ApiDeRespuesta.exito("Clave restablecida exitosamente")


