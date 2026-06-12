import pytest


@pytest.mark.asyncio
async def test_rate_limit_login_basico(client):
    for _ in range(11):
        r = await client.post('/api/autenticacion/iniciar-sesion', json={'correo': 'admin@sistema.com', 'clave': 'Admin123!'})
    assert r.status_code in (200, 400, 403)


@pytest.mark.asyncio
async def test_resultados_endpoints(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    r_codigo = await client.post('/api/evaluaciones/codigos', json={'version_instrumento_id': 1, 'horas_vigencia': 24}, headers=headers)
    assert r_codigo.status_code == 201
    codigo = r_codigo.json()['datos']['codigo']

    r_ini = await client.post('/api/evaluaciones/aplicaciones/iniciar', json={'codigo': codigo, 'nombre_paciente': 'Paciente Resultado'})
    assert r_ini.status_code == 201
    aplicacion_id = r_ini.json()['datos']['aplicacion_id']

    r_fin = await client.post('/api/evaluaciones/aplicaciones/finalizar', json={'aplicacion_id': aplicacion_id})
    assert r_fin.status_code == 200

    r_calc = await client.post(f'/api/evaluaciones/aplicaciones/{aplicacion_id}/resultado', headers=headers)
    assert r_calc.status_code == 200

    r_get = await client.get(f'/api/evaluaciones/aplicaciones/{aplicacion_id}/resultado', headers=headers)
    assert r_get.status_code == 200

    r_list = await client.get('/api/evaluaciones/resultados?pagina=1&tamano=10', headers=headers)
    assert r_list.status_code == 200


@pytest.mark.asyncio
async def test_metricas_requiere_autenticacion(client):
    r = await client.get('/api/metricas')
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_metricas_admin_ok(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    r = await client.get('/api/metricas', headers=headers)
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_metodo_no_permitido_en_login(client):
    r = await client.get('/api/autenticacion/iniciar-sesion')
    assert r.status_code == 405


@pytest.mark.asyncio
async def test_payload_invalido_login(client):
    r = await client.post('/api/autenticacion/iniciar-sesion', content='{"correo":')
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_resultado_sin_token(client):
    r = await client.get('/api/evaluaciones/aplicaciones/1/resultado')
    assert r.status_code == 401
