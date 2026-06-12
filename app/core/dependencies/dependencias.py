from app.modules.autenticacion.services.autenticacion_service import IAutenticacionService
from app.modules.autenticacion.services.impl.autenticacion_service_impl import AutenticacionServiceImpl
from app.modules.usuarios.services.usuario_service import IUsuarioService
from app.modules.usuarios.services.impl.usuario_service_impl import UsuarioServiceImpl
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.db.sesion import obtener_bd

def get_autenticacion_service() -> IAutenticacionService:
    return AutenticacionServiceImpl()

def get_usuario_service() -> IUsuarioService:
    return UsuarioServiceImpl()
