from fastapi import APIRouter, Depends

from app.core.config.metricas import auditoria_backend, metricas_backend
from app.core.responses.api_respuesta import ApiDeRespuesta
from app.core.security.seguridad import requiere_rol

metricas_router = APIRouter()


@metricas_router.get('', dependencies=[Depends(requiere_rol("ADMINISTRADOR"))])
async def obtener_metricas():
    return ApiDeRespuesta.exito(
        'Metricas obtenidas',
        {
            'tecnicas': metricas_backend.snapshot(),
            'auditoria': auditoria_backend.snapshot(),
        },
    )
