# [METODO] /api/usuarios/{usuario_id}

## Historia de Usuario
> **Como** SUPER_ADMIN (SaaS)
> **Quiero** solicitar el detalle específico de la cuenta de cualquier usuario
> **Para** auditar la información personal, estado y bitácora del usuario sin importar a qué empresa pertenezca.

## Criterios de Aceptación (Reglas de Negocio)
- Requiere rol SUPER_ADMIN.
- Si el `{usuario_id}` no existe, retorna 404.
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
  "mensaje": "Detalle de usuario.",
  "datos": {
    "id": 5,
    "nombre": "Juan"
  }
}
```
