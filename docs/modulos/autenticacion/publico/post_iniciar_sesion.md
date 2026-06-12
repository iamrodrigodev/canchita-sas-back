# [METODO] /api/autenticacion/iniciar-sesion

## Historia de Usuario
> **Como** Usuario No Autenticado (Público)
> **Quiero** iniciar sesión enviando mis credenciales
> **Para** obtener mis tokens JWT de acceso y refresco para navegar en la plataforma.

## Criterios de Aceptación (Reglas de Negocio)
- Si el usuario o clave son incorrectos, debe retornar código 401 sin especificar cuál de los dos falló (por seguridad).
- Si la cuenta está bloqueada o inactiva, debe retornar 403 Forbidden.
- **Códigos de Error:** 
  - `400 Bad Request`: Si los datos enviados no cumplen las validaciones.
  - `401 Unauthorized`: Si el token es inválido o no se envía.
  - `403 Forbidden`: Si el usuario no tiene los permisos (Usuario No Autenticado (Público)).
  - `404 Not Found`: Si el recurso solicitado no existe.

## Estructura Técnica

### Request
```json
{
  "correo": "juan@mail.com",
  "clave": "Segura123!"
}
```

### Response (2xx)
```json
{
  "estado": "exito",
  "mensaje": "Inicio de sesión exitoso.",
  "datos": {
    "token_acceso": "eyJhbG...",
    "token_refresco": "eyJhbG...",
    "tipo_token": "bearer"
  }
}
```
