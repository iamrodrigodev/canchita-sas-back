# [METODO] /api/usuario/{usuario_id}/perfil

## Historia de Usuario
> **Como** Usuario Autenticado (Cualquier Rol)
> **Quiero** enviar datos actualizados de mi perfil personal
> **Para** corregir mi nombre, apellido o número de teléfono si han cambiado.

## Criterios de Aceptación (Reglas de Negocio)
- El usuario solo puede modificar su propio perfil. Si envía un `{usuario_id}` que no coincide con su JWT, se deniega (403).
- Ciertos campos vitales (ej. Correo, Rol) no pueden modificarse desde este endpoint por seguridad.
- **Códigos de Error:** 
  - `400 Bad Request`: Si los datos enviados no cumplen las validaciones.
  - `401 Unauthorized`: Si el token es inválido o no se envía.
  - `403 Forbidden`: Si el usuario no tiene los permisos (Usuario Autenticado (Cualquier Rol)).
  - `404 Not Found`: Si el recurso solicitado no existe.

## Estructura Técnica

### Request
```json
{
  "nombre": "Admin Modificado",
  "apellidos": "Sistema Nuevo",
  "telefono": "999111222"
}
```

### Response (2xx)
```json
{
  "estado": "exito",
  "mensaje": "Perfil actualizado.",
  "datos": {
    "id": 1,
    "nombre": "Admin Modificado"
  }
}
```
