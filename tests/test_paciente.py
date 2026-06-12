import time

import pytest

from app.core.security.servicio_hash import ServicioHash
from app.modules.usuarios.models.usuario import Usuario
from app.modules.usuarios.repositories.usuario_repository import UsuarioRepository


async def _crear_paciente(correo: str, clave: str = 'Paciente123!') -> Usuario:
    existente = await UsuarioRepository.buscar_por_correo(correo)
    if existente:
        return existente
    usuario = Usuario(
        nombre='Paciente',
        apellidos='Prueba',
        correo=correo,
        clave=ServicioHash.hashear_contrasena(clave),
        telefono='+51900000000',
        rol_id=3,
        estado=1,
    )
    return await UsuarioRepository.guardar(usuario)


@pytest.mark.asyncio
async def test_paciente_denegado_en_rutas_admin(client):
    correo = f'paciente.admin.{time.time_ns()}@demo.com'
    await _crear_paciente(correo)
    login = await client.post('/api/autenticacion/iniciar-sesion', json={'correo': correo, 'clave': 'Paciente123!'})
    token = login.json().get('datos', {}).get('token_acceso')
    headers = {'Authorization': f'Bearer {token}'}

    r_usuarios = await client.get('/api/usuarios', headers=headers)
    assert r_usuarios.status_code == 403

    r_eval_admin = await client.get('/api/evaluaciones/aplicaciones', headers=headers)
    assert r_eval_admin.status_code == 403


@pytest.mark.asyncio
async def test_paciente_flujo_codigo_y_consulta_propia(client, auth_token):
    correo = f'paciente.flujo.{time.time_ns()}@demo.com'
    await _crear_paciente(correo)
    login_paciente = await client.post('/api/autenticacion/iniciar-sesion', json={'correo': correo, 'clave': 'Paciente123!'})
    token_paciente = login_paciente.json().get('datos', {}).get('token_acceso')
    headers_paciente = {'Authorization': f'Bearer {token_paciente}'}

    headers_admin = {'Authorization': f'Bearer {auth_token}'}
    r_codigo = await client.post('/api/evaluaciones/codigos', json={'version_instrumento_id': 1, 'horas_vigencia': 24}, headers=headers_admin)
    codigo = r_codigo.json()['datos']['codigo']

    r_ini = await client.post('/api/evaluaciones/aplicaciones/iniciar', json={'codigo': codigo, 'nombre_paciente': 'Paciente Logueado'}, headers=headers_paciente)
    assert r_ini.status_code == 201
    aplicacion_id = r_ini.json()['datos']['aplicacion_id']

    r_fin = await client.post('/api/evaluaciones/aplicaciones/finalizar', json={'aplicacion_id': aplicacion_id})
    assert r_fin.status_code == 200

    r_calc = await client.post(f'/api/evaluaciones/aplicaciones/{aplicacion_id}/resultado', headers=headers_admin)
    assert r_calc.status_code == 200

    r_list_eval = await client.get('/api/paciente/evaluaciones?pagina=1&tamano=10', headers=headers_paciente)
    assert r_list_eval.status_code == 200
    assert r_list_eval.json()['datos']['total'] >= 1

    r_det_eval = await client.get(f'/api/paciente/evaluaciones/{aplicacion_id}', headers=headers_paciente)
    assert r_det_eval.status_code == 200

    r_list_res = await client.get('/api/paciente/resultados?pagina=1&tamano=10', headers=headers_paciente)
    assert r_list_res.status_code == 200

    r_det_res = await client.get(f'/api/paciente/resultados/{aplicacion_id}', headers=headers_paciente)
    assert r_det_res.status_code == 200


@pytest.mark.asyncio
async def test_paciente_acceso_cruzado_denegado(client, auth_token):
    correo_a = f'paciente.a.{time.time_ns()}@demo.com'
    correo_b = f'paciente.b.{time.time_ns()}@demo.com'
    await _crear_paciente(correo_a)
    await _crear_paciente(correo_b)

    login_a = await client.post('/api/autenticacion/iniciar-sesion', json={'correo': correo_a, 'clave': 'Paciente123!'})
    login_b = await client.post('/api/autenticacion/iniciar-sesion', json={'correo': correo_b, 'clave': 'Paciente123!'})
    token_a = login_a.json().get('datos', {}).get('token_acceso')
    token_b = login_b.json().get('datos', {}).get('token_acceso')
    headers_a = {'Authorization': f'Bearer {token_a}'}
    headers_b = {'Authorization': f'Bearer {token_b}'}

    headers_admin = {'Authorization': f'Bearer {auth_token}'}
    r_codigo = await client.post('/api/evaluaciones/codigos', json={'version_instrumento_id': 1, 'horas_vigencia': 24}, headers=headers_admin)
    codigo = r_codigo.json()['datos']['codigo']

    r_ini_a = await client.post('/api/evaluaciones/aplicaciones/iniciar', json={'codigo': codigo, 'nombre_paciente': 'Paciente A'}, headers=headers_a)
    aplicacion_id_a = r_ini_a.json()['datos']['aplicacion_id']

    r_denegado = await client.get(f'/api/paciente/evaluaciones/{aplicacion_id_a}', headers=headers_b)
    assert r_denegado.status_code == 403
