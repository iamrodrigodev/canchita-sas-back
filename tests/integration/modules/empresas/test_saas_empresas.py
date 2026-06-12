import pytest
import pytest_asyncio
from httpx import AsyncClient

# Dependiendo del auth_token, seremos SUPER_ADMIN porque login_payload_ok inicia sesión con admin@sistema.com

@pytest.mark.asyncio
async def test_crear_y_listar_empresa_api(client: AsyncClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    import uuid
    unico = str(uuid.uuid4())[:8]

    # 1. Crear empresa
    payload_crear = {
        "nombre_comercial": "Mi Canchita SaaS API",
        "razon_social": "SaaS API SAC",
        "ruc": f"102{unico}",
        "subdominio": f"api{unico}",
        "usuario_dueño_id": 1
    }
    
    res_crear = await client.post("/api/saas/empresas", json=payload_crear, headers=headers)
    assert res_crear.status_code == 201
    datos_creados = res_crear.json().get("datos", {})
    assert datos_creados["nombre_comercial"] == "Mi Canchita SaaS API"
    empresa_id = datos_creados["id"]
    
    # 2. Listar empresas
    res_listar = await client.get("/api/saas/empresas?busqueda=SaaS API", headers=headers)
    assert res_listar.status_code == 200
    datos_lista = res_listar.json().get("datos", {})
    assert datos_lista["total"] >= 1
    
    # 3. Obtener detalle
    res_detalle = await client.get(f"/api/saas/empresas/{empresa_id}", headers=headers)
    assert res_detalle.status_code == 200
    assert res_detalle.json()["datos"]["id"] == empresa_id
    
    # 4. Actualizar
    payload_actualizar = {
        "nombre_comercial": "Mi Canchita SaaS API V2",
        "razon_social": "SaaS API SAC",
        "ruc": f"102{unico}",
        "subdominio": f"api{unico}v2"
    }
    res_actualizar = await client.put(f"/api/saas/empresas/{empresa_id}", json=payload_actualizar, headers=headers)
    assert res_actualizar.status_code == 200
    assert res_actualizar.json()["datos"]["subdominio"] == f"api{unico}v2"
    
    # 5. Suspender
    payload_estado = {"estado": 2}
    res_estado = await client.patch(f"/api/saas/empresas/{empresa_id}/estado", json=payload_estado, headers=headers)
    assert res_estado.status_code == 200
    assert res_estado.json()["datos"]["estado"] == 2

@pytest.mark.asyncio
async def test_seguridad_sin_token(client: AsyncClient):
    res = await client.get("/api/saas/empresas")
    assert res.status_code == 401
