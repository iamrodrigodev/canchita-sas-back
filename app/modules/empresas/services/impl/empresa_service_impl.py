import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.db.sesion import SessionLocal
from app.core.exceptions.errores_personalizados import ExcepcionDeNegocio
from app.core.exceptions.mensajes_error import MensajesDeError
from app.modules.empresas.models.empresa import Empresa
from app.modules.empresas.models.rol_empresa import RolEmpresa
from app.modules.empresas.models.usuario_empresa import UsuarioEmpresa
from app.modules.empresas.enums.roles_empresa import RolesEmpresa
from app.modules.empresas.schemas.peticion.empresa_crear_peticion import EmpresaCrearPeticion
from app.modules.empresas.schemas.respuesta.empresa_respuesta import EmpresaRespuesta
from app.modules.empresas.services.empresa_service import IEmpresaService
from app.modules.usuarios.models.usuario import Usuario

logger = logging.getLogger("fastapi")

class EmpresaServiceImpl(IEmpresaService):
    
    async def crear_empresa(self, peticion: EmpresaCrearPeticion, saas_admin_id: int) -> EmpresaRespuesta:
        async with SessionLocal() as session:
            try:
                # 1. Verificar si el subdominio o ruc ya existen
                stmt_existe = select(Empresa).where(
                    (Empresa.subdominio == peticion.subdominio) | 
                    ((Empresa.ruc == peticion.ruc) & (Empresa.ruc.is_not(None)))
                )
                existe = (await session.execute(stmt_existe)).scalars().first()
                if existe:
                    raise ExcepcionDeNegocio("El subdominio o RUC ya se encuentra registrado.")

                # 2. Verificar que el usuario dueño existe
                stmt_usuario = select(Usuario).where(Usuario.id == peticion.usuario_dueño_id)
                usuario = (await session.execute(stmt_usuario)).scalars().first()
                if not usuario:
                    raise ExcepcionDeNegocio(MensajesDeError.USUARIO_NO_ENCONTRADO)

                # 3. Obtener el ID del rol local "ADMIN_EMPRESA"
                stmt_rol = select(RolEmpresa).where(RolEmpresa.nombre == RolesEmpresa.ADMIN_EMPRESA.value)
                rol_admin = (await session.execute(stmt_rol)).scalars().first()
                if not rol_admin:
                    raise ExcepcionDeNegocio("Error de consistencia: Rol ADMIN_EMPRESA no existe.")

                # 4. Crear la Empresa
                nueva_empresa = Empresa(
                    nombre_comercial=peticion.nombre_comercial,
                    razon_social=peticion.razon_social,
                    ruc=peticion.ruc,
                    subdominio=peticion.subdominio
                )
                session.add(nueva_empresa)
                await session.flush() # Para obtener el ID

                # 5. Vincular al usuario como ADMIN_EMPRESA
                vinculo = UsuarioEmpresa(
                    usuario_id=usuario.id,
                    empresa_id=nueva_empresa.id,
                    rol_empresa_id=rol_admin.id
                )
                session.add(vinculo)
                
                await session.commit()
                await session.refresh(nueva_empresa)
                
                logger.info(f"[AUDITORIA] empresa_creada saas_admin={saas_admin_id} empresa_id={nueva_empresa.id} dueño={usuario.id}")
                
                return EmpresaRespuesta.model_validate(nueva_empresa)
                
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Error BD al crear empresa: {str(e)}")
                raise ExcepcionDeNegocio(MensajesDeError.ERROR_GENERAL)

    async def listar_empresas(self, pagina: int, tamano: int, busqueda: str | None, estado: int | None) -> EmpresaPaginacionRespuesta:
        from app.modules.empresas.repositories.empresa_repository import EmpresaRepository
        empresas, total = await EmpresaRepository.listar_paginado(pagina, tamano, busqueda, estado)
        items = [EmpresaRespuesta.model_validate(empresa) for empresa in empresas]
        return EmpresaPaginacionRespuesta(items=items, total=total, pagina=pagina, tamano=tamano)

    async def obtener_empresa(self, empresa_id: int) -> EmpresaRespuesta:
        from app.modules.empresas.repositories.empresa_repository import EmpresaRepository
        empresa = await EmpresaRepository.buscar_por_id(empresa_id)
        if not empresa:
            raise ExcepcionDeNegocio("Empresa no encontrada")
        return EmpresaRespuesta.model_validate(empresa)

    async def actualizar_empresa(self, empresa_id: int, peticion: EmpresaGestionActualizarPeticion, saas_admin_id: int) -> EmpresaRespuesta:
        from app.modules.empresas.repositories.empresa_repository import EmpresaRepository
        empresa = await EmpresaRepository.buscar_por_id(empresa_id)
        if not empresa:
            raise ExcepcionDeNegocio("Empresa no encontrada")

        empresa.nombre_comercial = peticion.nombre_comercial
        empresa.razon_social = peticion.razon_social
        empresa.ruc = peticion.ruc
        empresa.subdominio = peticion.subdominio
        
        guardado = await EmpresaRepository.guardar(empresa)
        logger.info(f"[AUDITORIA] empresa_actualizada saas_admin={saas_admin_id} empresa_id={guardado.id}")
        return EmpresaRespuesta.model_validate(guardado)

    async def cambiar_estado_empresa(self, empresa_id: int, estado: int, saas_admin_id: int) -> EmpresaRespuesta:
        from app.modules.empresas.repositories.empresa_repository import EmpresaRepository
        empresa = await EmpresaRepository.buscar_por_id(empresa_id)
        if not empresa:
            raise ExcepcionDeNegocio("Empresa no encontrada")

        empresa.estado = estado
        guardado = await EmpresaRepository.guardar(empresa)
        logger.info(f"[AUDITORIA] empresa_estado_cambiado saas_admin={saas_admin_id} empresa_id={guardado.id} estado={estado}")
        return EmpresaRespuesta.model_validate(guardado)

def get_empresa_service() -> IEmpresaService:
    return EmpresaServiceImpl()
