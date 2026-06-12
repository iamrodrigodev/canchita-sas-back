from fastapi import Request
from app.core.exceptions.errores_personalizados import ExcepcionDeNegocio
from app.core.exceptions.mensajes_error import MensajesDeError
from app.utils.rate_limit_util import limitador_memoria
from app.core.config.ajustes import ajustes


def _ip(request: Request) -> str:
    return request.client.host if request.client else "0.0.0.0"


def validar_rate_limit_login(request: Request, correo: str):
    if ajustes.ENTORNO.lower() in {"test", "testing"}:
        return
    if not limitador_memoria.permitido(f"login_ip:{_ip(request)}", 20, 60):
        raise ExcepcionDeNegocio(MensajesDeError.ACCESO_DENEGADO, detalles="Demasiados intentos. Intente nuevamente.")
    if not limitador_memoria.permitido(f"login_correo:{correo.lower()}", 10, 60):
        raise ExcepcionDeNegocio(MensajesDeError.ACCESO_DENEGADO, detalles="Demasiados intentos. Intente nuevamente.")


def validar_rate_limit_refresh(request: Request, token_refresco: str):
    if ajustes.ENTORNO.lower() in {"test", "testing"}:
        return
    if not limitador_memoria.permitido(f"refresh_ip:{_ip(request)}", 30, 60):
        raise ExcepcionDeNegocio(MensajesDeError.ACCESO_DENEGADO, detalles="Demasiadas solicitudes. Intente nuevamente.")
    sufijo = token_refresco[-12:] if token_refresco else "vacio"
    if not limitador_memoria.permitido(f"refresh_token:{sufijo}", 15, 60):
        raise ExcepcionDeNegocio(MensajesDeError.ACCESO_DENEGADO, detalles="Demasiadas solicitudes. Intente nuevamente.")


def validar_rate_limit_recuperacion(request: Request, correo: str):
    if ajustes.ENTORNO.lower() in {"test", "testing"}:
        return
    if not limitador_memoria.permitido(f"recup_ip:{_ip(request)}", 15, 60):
        raise ExcepcionDeNegocio(MensajesDeError.ACCESO_DENEGADO, detalles="Demasiadas solicitudes. Intente nuevamente.")
    if not limitador_memoria.permitido(f"recup_correo:{correo.lower()}", 6, 300):
        raise ExcepcionDeNegocio(MensajesDeError.ACCESO_DENEGADO, detalles="Demasiadas solicitudes. Intente nuevamente.")


def validar_rate_limit_inicio_aplicacion(request: Request, codigo: str):
    if ajustes.ENTORNO.lower() in {"test", "testing"}:
        return
    if not limitador_memoria.permitido(f"eval_ini_ip:{_ip(request)}", 30, 60):
        raise ExcepcionDeNegocio(MensajesDeError.ACCESO_DENEGADO, detalles="Demasiadas solicitudes. Intente nuevamente.")
    if not limitador_memoria.permitido(f"eval_ini_codigo:{(codigo or '').upper()}", 20, 60):
        raise ExcepcionDeNegocio(MensajesDeError.ACCESO_DENEGADO, detalles="Demasiadas solicitudes. Intente nuevamente.")


def validar_rate_limit_responder(request: Request, aplicacion_id: int):
    if ajustes.ENTORNO.lower() in {"test", "testing"}:
        return
    if not limitador_memoria.permitido(f"eval_resp_ip:{_ip(request)}", 120, 60):
        raise ExcepcionDeNegocio(MensajesDeError.ACCESO_DENEGADO, detalles="Demasiadas solicitudes. Intente nuevamente.")
    if not limitador_memoria.permitido(f"eval_resp_apl:{aplicacion_id}", 80, 60):
        raise ExcepcionDeNegocio(MensajesDeError.ACCESO_DENEGADO, detalles="Demasiadas solicitudes. Intente nuevamente.")


def validar_rate_limit_finalizar(request: Request, aplicacion_id: int):
    if ajustes.ENTORNO.lower() in {"test", "testing"}:
        return
    if not limitador_memoria.permitido(f"eval_fin_ip:{_ip(request)}", 40, 60):
        raise ExcepcionDeNegocio(MensajesDeError.ACCESO_DENEGADO, detalles="Demasiadas solicitudes. Intente nuevamente.")
    if not limitador_memoria.permitido(f"eval_fin_apl:{aplicacion_id}", 10, 60):
        raise ExcepcionDeNegocio(MensajesDeError.ACCESO_DENEGADO, detalles="Demasiadas solicitudes. Intente nuevamente.")


