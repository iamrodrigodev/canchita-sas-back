import pytest
from app.modules.empresas.services.impl.empresa_service_impl import EmpresaServiceImpl
from app.modules.empresas.schemas.peticion.empresa_crear_peticion import EmpresaCrearPeticion
from app.modules.empresas.schemas.peticion.empresa_gestion_peticion import EmpresaGestionActualizarPeticion
from app.core.exceptions.errores_personalizados import ExcepcionDeNegocio
from app.db.inicializar_bd import inicializar_datos
from app.modules.usuarios.repositories.usuario_repository import UsuarioRepository

@pytest.mark.asyncio
async def test_crear_y_gestionar_empresa_flujo_completo():
    await inicializar_datos()
    servicio = EmpresaServiceImpl()
    
    # 1. Obtener usuario admin existente (id 1)
    usuario_admin = await UsuarioRepository.buscar_por_correo("admin@sistema.com")
    assert usuario_admin is not None
    saas_admin_id = int(usuario_admin.id)
    
    import uuid
    unico = str(uuid.uuid4())[:8]
    
    # 2. Crear nueva empresa
    peticion_crear = EmpresaCrearPeticion(
        nombre_comercial="Canchas Test",
        razon_social="Test SAC",
        ruc=f"123{unico}",
        subdominio=f"test{unico}",
        usuario_dueño_id=saas_admin_id
    )
    
    empresa_creada = await servicio.crear_empresa(peticion_crear, saas_admin_id)
    assert empresa_creada.id > 0
    assert empresa_creada.nombre_comercial == "Canchas Test"
    assert empresa_creada.estado == 1
    
    # 3. Intentar crear con mismo RUC debe fallar
    with pytest.raises(ExcepcionDeNegocio) as excinfo:
        await servicio.crear_empresa(peticion_crear, saas_admin_id)
    assert "ya se encuentra registrado" in str(excinfo.value)
    
    # 4. Obtener empresa
    empresa_obtenida = await servicio.obtener_empresa(empresa_creada.id)
    assert empresa_obtenida.subdominio == f"test{unico}"
    
    # 5. Listar empresas
    paginacion = await servicio.listar_empresas(pagina=1, tamano=10, busqueda="Test SAC", estado=None)
    assert paginacion.total >= 1
    assert any(e.id == empresa_creada.id for e in paginacion.items)
    
    # 6. Actualizar empresa
    peticion_actualizar = EmpresaGestionActualizarPeticion(
        nombre_comercial="Canchas Test Editadas",
        razon_social="Test Editado SAC",
        ruc=f"123{unico}",
        subdominio=f"test{unico}edit"
    )
    empresa_actualizada = await servicio.actualizar_empresa(empresa_creada.id, peticion_actualizar, saas_admin_id)
    assert empresa_actualizada.nombre_comercial == "Canchas Test Editadas"
    
    # 7. Cambiar estado a Suspendido (2)
    empresa_suspendida = await servicio.cambiar_estado_empresa(empresa_creada.id, 2, saas_admin_id)
    assert empresa_suspendida.estado == 2
