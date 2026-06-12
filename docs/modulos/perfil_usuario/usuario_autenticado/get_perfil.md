# [METODO] /api/usuario/perfil

## Historia de Usuario
> **Como** Usuario Autenticado (Cualquier Rol)
> **Quiero** solicitar la información de mi propio perfil
> **Para** visualizar mis datos personales y rol actual dentro de Mi Cuenta.

## Criterios de Aceptación (Reglas de Negocio)
- El `usuario_id` es inyectado desde el JWT por el Middleware de Seguridad, no por la URL.
- No se devuelve información sensible como el hash de la clave.
- **Códigos de Error:** 
  - `400 Bad Request`: Si los datos enviados no cumplen las validaciones.
  - `401 Unauthorized`: Si el token es inválido o no se envía.
  - `403 Forbidden`: Si el usuario no tiene los permisos (Usuario Autenticado (Cualquier Rol)).
  - `404 Not Found`: Si el recurso solicitado no existe.

## Estructura Técnica

### Request
```json
{}
```

### Response (2xx)
```json
{
  "estado": "exito",
  "mensaje": "Perfil obtenido.",
  "datos": {
    "id": 1,
    "nombre": "Admin",
    "correo": "admin@sistema.com"
  }
}
```
