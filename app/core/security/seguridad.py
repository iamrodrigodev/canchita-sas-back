from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security.servicio_jwt import ServicioJwt
from app.modules.usuarios.repositories.usuario_repository import UsuarioRepository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/autenticacion/iniciar-sesion")


async def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    usuario_id = ServicioJwt.decodificar_token(token)
    if not usuario_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Fallo en la autenticacion, intente nuevamente",
            headers={"WWW-Authenticate": "Bearer"},
        )

    usuario = await UsuarioRepository.buscar_por_id(usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if getattr(usuario, "estado", 1) != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return usuario


async def obtener_usuario_actual_id(usuario_actual=Depends(obtener_usuario_actual)) -> int:
    return int(usuario_actual.id)


def requiere_rol(rol_nombre: str):
    def verificador_rol(usuario=Depends(obtener_usuario_actual)):
        if usuario.rol.nombre != rol_nombre:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado: no tiene los permisos necesarios",
            )
        return usuario

    return verificador_rol


def verificar_propietario_o_admin(usuario_objetivo_id: int, usuario_actual) -> None:
    es_admin = usuario_actual.rol and usuario_actual.rol.nombre == "ADMINISTRADOR"
    es_propietario = int(usuario_actual.id) == int(usuario_objetivo_id)
    if not (es_admin or es_propietario):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado: no puede acceder a recursos de otro usuario",
        )


def verificar_propietario(usuario_objetivo_id: int, usuario_actual) -> None:
    if int(usuario_actual.id) != int(usuario_objetivo_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado: no puede acceder a recursos de otro usuario",
        )

from fastapi import Header

async def obtener_usuario_actual_opcional(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.startswith('Bearer '):
        return None
    token = authorization.split(' ', 1)[1].strip()
    usuario_id = ServicioJwt.decodificar_token(token)
    if not usuario_id:
        return None
    usuario = await UsuarioRepository.buscar_por_id(usuario_id)
    if not usuario or getattr(usuario, 'estado', 1) != 1:
        return None
    return usuario

