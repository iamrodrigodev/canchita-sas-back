# [METODO] /api/usuarios/{usuario_id}

## Historia de Usuario
> **Como** SUPER_ADMIN (SaaS)
> **Quiero** solicitar la eliminación física (hard-delete) de la cuenta de un usuario
> **Para** eliminar permanentemente el registro de la base de datos matriz por violaciones graves o solicitudes legales (Derecho al olvido).

## Criterios de Aceptación (Reglas de Negocio)
- Falla si el usuario ya tiene registros transaccionales atados (ej. Pagos, Reservas) por Foreign Keys. En esos casos se recomienda el `PATCH estado`.
- Requiere rol SUPER_ADMIN.
- **Códigos de Error:** 
  - `400 Bad Request`: Si los datos enviados no cumplen las validaciones.
  - `401 Unauthorized`: Si el token es inválido o no se envía.
  - `403 Forbidden`: Si el usuario no tiene los permisos (SUPER_ADMIN (SaaS)).
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
  "mensaje": "Usuario eliminado.",
  "datos": null
}
```
