# [METODO] /api/usuarios/{usuario_id}/estado

## Historia de Usuario
> **Como** SUPER_ADMIN (SaaS)
> **Quiero** enviar un nuevo `estado` numérico (1 = Activo, 0 = Inactivo) a una cuenta
> **Para** bloquear el acceso a la plataforma matriz a usuarios maliciosos (ban global).

## Criterios de Aceptación (Reglas de Negocio)
- Si se inhabilita, el usuario perderá acceso inmediato a toda la plataforma.
- Un Super Admin no puede inhabilitar su propia cuenta (protección contra lock-out).
- **Códigos de Error:** 
  - `400 Bad Request`: Si los datos enviados no cumplen las validaciones.
  - `401 Unauthorized`: Si el token es inválido o no se envía.
  - `403 Forbidden`: Si el usuario no tiene los permisos (SUPER_ADMIN (SaaS)).
  - `404 Not Found`: Si el recurso solicitado no existe.

## Estructura Técnica

### Request
```json
{
  "estado": 0
}
```

### Response (2xx)
```json
{
  "estado": "exito",
  "mensaje": "Estado actualizado.",
  "datos": {
    "estado": 0
  }
}
```
