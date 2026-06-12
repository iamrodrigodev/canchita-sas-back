import os
import asyncio
import bcrypt
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.db.sesion import SessionLocal, engine, Base
from app.modules.usuarios.models.rol import Rol
from app.modules.usuarios.models.usuario import Usuario
from app.modules.ubicacion.models.departamento import Departamento
from app.modules.ubicacion.models.provincia import Provincia
from app.modules.ubicacion.models.distrito import Distrito
from app.modules.autenticacion.models.token_refresco import TokenRefresco
from app.modules.autenticacion.models.credencial_usuario import CredencialUsuario
from app.modules.autenticacion.models.estado_login_usuario import EstadoLoginUsuario
from app.modules.autenticacion.models.token_recuperacion_clave import TokenRecuperacionClave
from app.modules.estado.models.registro_auditoria import RegistroAuditoria
from app.modules.empresas.models.empresa import Empresa
from app.modules.empresas.models.rol_empresa import RolEmpresa
from app.modules.empresas.models.usuario_empresa import UsuarioEmpresa
import logging
from app.core.config.ajustes import ajustes

_ = (
    bcrypt,
    Rol,
    Usuario,
    Departamento,
    Provincia,
    Distrito,
    TokenRefresco,
    CredencialUsuario,
    EstadoLoginUsuario,
    TokenRecuperacionClave,
    RegistroAuditoria,
    Empresa,
    RolEmpresa,
    UsuarioEmpresa,
)

logger = logging.getLogger("fastapi")


def _leer_sentencias_sql(sql_path: str) -> list[str]:
    with open(sql_path, "r", encoding="utf-8-sig") as archivo_sql:
        contenido = archivo_sql.read()
    sentencias = []
    acumulado: list[str] = []
    for linea in contenido.splitlines():
        texto = linea.strip()
        if not texto or texto.startswith("--"):
            continue
        acumulado.append(linea)
    bloque = "\n".join(acumulado)
    for sentencia in bloque.split(";"):
        limpia = sentencia.strip()
        if limpia:
            sentencias.append(limpia)
    return sentencias


async def _asegurar_esquemas():
    async with engine.begin() as conn:
        try:
            await conn.execute(text("CREATE SCHEMA IF NOT EXISTS autenticacion;"))
            await conn.execute(text("CREATE SCHEMA IF NOT EXISTS ubicacion;"))
            await conn.execute(text("CREATE SCHEMA IF NOT EXISTS estado;"))
            await conn.execute(text("CREATE SCHEMA IF NOT EXISTS empresas;"))
            logger.info("Esquemas verificados")
        except SQLAlchemyError as e:
            logger.error(f"Error al crear esquemas: {str(e)}")
            if ajustes.DB_FAIL_FAST:
                raise


async def cargar_catalogos_sql():
    async with SessionLocal() as session:
        try:
            sql_path = os.path.join(os.path.dirname(__file__), 'sql', 'ubicacion_peru.sql')
            if os.path.exists(sql_path):
                for statement in _leer_sentencias_sql(sql_path):
                    await session.execute(text(statement))
                await session.commit()
                logger.info("Catalogo de ubicacion (SQL) cargado exitosamente")
            else:
                logger.warning(f"Archivo SQL no encontrado en la ruta: {sql_path}")
        except IntegrityError:
            await session.rollback()
            logger.info("Catalogo de ubicacion ya existe (se ignoro el insert duplicado)")
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Error al cargar catalogo SQL: {str(e)}")
            if ajustes.DB_FAIL_FAST:
                raise


async def sembrar_usuarios_base():
    async with SessionLocal() as session:
        try:
            sql_path = os.path.join(os.path.dirname(__file__), 'sql', 'usuarios_semilla.sql')
            if os.path.exists(sql_path):
                for statement in _leer_sentencias_sql(sql_path):
                    await session.execute(text(statement))
                await session.commit()
                logger.info("Usuarios semilla cargados exitosamente (Admin y Usuario)")
            else:
                logger.warning(f"Archivo SQL de usuarios no encontrado: {sql_path}")
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Error al cargar usuarios semilla: {str(e)}")
            if ajustes.DB_FAIL_FAST:
                raise


async def sembrar_roles_empresa():
    async with SessionLocal() as session:
        try:
            roles = ['ADMIN_EMPRESA', 'CAJERO', 'CLIENTE']
            for rol_nombre in roles:
                result = await session.execute(
                    text("SELECT id FROM empresas.roles_empresa WHERE nombre = :nombre"),
                    {'nombre': rol_nombre}
                )
                if not result.scalar():
                    await session.execute(
                        text("INSERT INTO empresas.roles_empresa (nombre) VALUES (:nombre)"),
                        {'nombre': rol_nombre}
                    )
            await session.commit()
            logger.info("Roles de empresa semilla verificados exitosamente")
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Error al cargar roles de empresa: {str(e)}")
            if ajustes.DB_FAIL_FAST:
                raise


async def inicializar_datos():
    await _asegurar_esquemas()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await cargar_catalogos_sql()
    await sembrar_usuarios_base()
    await sembrar_roles_empresa()


if __name__ == "__main__":
    asyncio.run(inicializar_datos())
