import logging
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.db.sesion import SessionLocal
from app.modules.empresas.models.empresa import Empresa
from app.modules.empresas.models.usuario_empresa import UsuarioEmpresa

logger = logging.getLogger("fastapi")

class EmpresaRepository:
    @staticmethod
    def _query_base():
        return (
            select(Empresa)
            .options(
                selectinload(Empresa.usuarios_empresa)
                .selectinload(UsuarioEmpresa.usuario)
            )
        )

    @staticmethod
    async def buscar_por_id(id: int):
        async with SessionLocal() as session:
            result = await session.execute(EmpresaRepository._query_base().filter_by(id=id))
            return result.scalars().first()

    @staticmethod
    async def listar_paginado(pagina: int, tamano: int, busqueda: str | None, estado: int | None):
        async with SessionLocal() as session:
            query = EmpresaRepository._query_base()
            count_query = select(func.count(Empresa.id))

            if busqueda:
                patron = f"%{busqueda.strip().lower()}%"
                filtro = (func.lower(Empresa.nombre_comercial).like(patron)) | \
                         (func.lower(Empresa.razon_social).like(patron)) | \
                         (func.lower(Empresa.ruc).like(patron))
                query = query.where(filtro)
                count_query = count_query.where(filtro)
                
            if estado is not None:
                query = query.where(Empresa.estado == estado)
                count_query = count_query.where(Empresa.estado == estado)

            query = query.order_by(Empresa.id.desc()).offset((pagina - 1) * tamano).limit(tamano)

            total_result = await session.execute(count_query)
            total = int(total_result.scalar() or 0)
            result = await session.execute(query)
            return result.scalars().all(), total

    @staticmethod
    async def guardar(empresa):
        async with SessionLocal() as session:
            try:
                if getattr(empresa, "id", None) is None:
                    session.add(empresa)
                    entidad = empresa
                else:
                    entidad = await session.merge(empresa)
                await session.commit()
                await session.refresh(entidad)
                return entidad
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Error al guardar empresa {empresa.nombre_comercial}: {str(e)}")
                raise

    @staticmethod
    async def eliminar(empresa):
        async with SessionLocal() as session:
            try:
                merged_empresa = await session.merge(empresa)
                await session.delete(merged_empresa)
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Error al eliminar empresa {empresa.id}: {str(e)}")
                raise
