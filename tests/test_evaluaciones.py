import pytest


@pytest.mark.asyncio
async def test_flujo_evaluaciones_saas(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    cfg = {
        "tiempo_por_pregunta_segundos": 25,
        "tiempo_advertencia_segundos": 7,
        "permitir_auto_completado": True,
        "solicitar_telefono_paciente": False,
        "solicitar_documento_paciente": False,
    }
    r_cfg = await client.put("/api/evaluaciones/configuracion", json=cfg, headers=headers)
    assert r_cfg.status_code == 200

    r_codigo = await client.post(
        "/api/evaluaciones/codigos",
        json={"version_instrumento_id": 1, "horas_vigencia": 24},
        headers=headers,
    )
    assert r_codigo.status_code == 201
    codigo = r_codigo.json()["datos"]["codigo"]

    r_ini = await client.post(
        "/api/evaluaciones/aplicaciones/iniciar",
        json={"codigo": codigo, "nombre_paciente": "Paciente Demo"},
    )
    assert r_ini.status_code == 201
    aplicacion_id = r_ini.json()["datos"]["aplicacion_id"]

    r_fin = await client.post(
        "/api/evaluaciones/aplicaciones/finalizar",
        json={"aplicacion_id": aplicacion_id},
    )
    assert r_fin.status_code == 200

    r_lista = await client.get("/api/evaluaciones/aplicaciones?pagina=1&tamano=5", headers=headers)
    assert r_lista.status_code == 200

    r_detalle = await client.get(f"/api/evaluaciones/aplicaciones/{aplicacion_id}", headers=headers)
    assert r_detalle.status_code == 200

    r_reporte = await client.get(f"/api/evaluaciones/aplicaciones/{aplicacion_id}/reporte", headers=headers)
    assert r_reporte.status_code == 200
    assert "text/csv" in r_reporte.headers.get("content-type", "")


@pytest.mark.asyncio
async def test_evaluaciones_tenant_denegado(client):
    login_admin = await client.post('/api/autenticacion/iniciar-sesion', json={'correo': 'admin@sistema.com', 'clave': 'Admin123!'})
    token_admin = login_admin.json().get('datos', {}).get('token_acceso')

    login_usuario = await client.post('/api/autenticacion/iniciar-sesion', json={'correo': 'usuario@demo.com', 'clave': 'Admin123!'})
    token_usuario = login_usuario.json().get('datos', {}).get('token_acceso')

    headers_admin = {'Authorization': f'Bearer {token_admin}'}
    headers_usuario = {'Authorization': f'Bearer {token_usuario}'}

    r_codigo = await client.post('/api/evaluaciones/codigos', json={'version_instrumento_id': 1, 'horas_vigencia': 24}, headers=headers_admin)
    codigo = r_codigo.json()['datos']['codigo']

    r_ini = await client.post('/api/evaluaciones/aplicaciones/iniciar', json={'codigo': codigo, 'nombre_paciente': 'Paciente X'})
    aplicacion_id = r_ini.json()['datos']['aplicacion_id']

    r_denegado = await client.get(f'/api/evaluaciones/aplicaciones/{aplicacion_id}', headers=headers_usuario)
    assert r_denegado.status_code == 404


@pytest.mark.asyncio
async def test_evaluaciones_requiere_auth_en_listado(client):
    response = await client.get('/api/evaluaciones/aplicaciones')
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_evaluaciones_version_no_disponible(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = await client.post('/api/evaluaciones/codigos', json={'version_instrumento_id': 999999, 'horas_vigencia': 1}, headers=headers)
    assert response.status_code in (400, 404)


@pytest.mark.asyncio
async def test_evaluaciones_paginacion_limite(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = await client.get('/api/evaluaciones/aplicaciones?pagina=1&tamano=9999', headers=headers)
    assert response.status_code == 200
    datos = response.json().get('datos', {})
    assert datos.get('tamano') == 100

@pytest.mark.asyncio
async def test_evaluaciones_tenant_denegado_en_reporte_y_resultados(client):
    login_admin = await client.post('/api/autenticacion/iniciar-sesion', json={'correo': 'admin@sistema.com', 'clave': 'Admin123!'})
    token_admin = login_admin.json().get('datos', {}).get('token_acceso')

    login_usuario = await client.post('/api/autenticacion/iniciar-sesion', json={'correo': 'usuario@demo.com', 'clave': 'Admin123!'})
    token_usuario = login_usuario.json().get('datos', {}).get('token_acceso')

    headers_admin = {'Authorization': f'Bearer {token_admin}'}
    headers_usuario = {'Authorization': f'Bearer {token_usuario}'}

    r_codigo = await client.post('/api/evaluaciones/codigos', json={'version_instrumento_id': 1, 'horas_vigencia': 24}, headers=headers_admin)
    codigo = r_codigo.json()['datos']['codigo']

    r_ini = await client.post('/api/evaluaciones/aplicaciones/iniciar', json={'codigo': codigo, 'nombre_paciente': 'Paciente Privado'})
    aplicacion_id = r_ini.json()['datos']['aplicacion_id']

    r_fin = await client.post('/api/evaluaciones/aplicaciones/finalizar', json={'aplicacion_id': aplicacion_id})
    assert r_fin.status_code == 200

    r_calc_admin = await client.post(f'/api/evaluaciones/aplicaciones/{aplicacion_id}/resultado', headers=headers_admin)
    assert r_calc_admin.status_code == 200

    r_reporte_denegado = await client.get(f'/api/evaluaciones/aplicaciones/{aplicacion_id}/reporte', headers=headers_usuario)
    assert r_reporte_denegado.status_code in (403, 404)

    r_resultado_denegado = await client.get(f'/api/evaluaciones/aplicaciones/{aplicacion_id}/resultado', headers=headers_usuario)
    assert r_resultado_denegado.status_code in (403, 404)

    r_calculo_denegado = await client.post(f'/api/evaluaciones/aplicaciones/{aplicacion_id}/resultado', headers=headers_usuario)
    assert r_calculo_denegado.status_code in (403, 404)
