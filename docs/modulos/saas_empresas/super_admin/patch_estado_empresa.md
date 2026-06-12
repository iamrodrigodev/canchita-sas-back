# [METODO] /api/saas/empresas/{empresa_id}/estado

## Historia de Usuario
> **Como** SUPER_ADMIN (SaaS)
> **Quiero** enviar un comando de cambio de estado sobre un tenant completo (1=Activo, 2=Suspendido)
> **Para** suspender de manera fulminante el servicio a una empresa por falta de pago.

## Criterios de Aceptación (Reglas de Negocio)
- El cambio de estado debe ser instantáneo.
- El Guardián SaaS interceptará cualquier Request subsecuente hacia recursos de esta empresa y bloqueará (403 Forbidden) al personal de dicha empresa.
- **Códigos de Error:** 
  - `400 Bad Request`: Si los datos enviados no cumplen las validaciones.
  - `401 Unauthorized`: Si el token es inválido o no se envía.
  - `403 Forbidden`: Si el usuario no tiene los permisos (SUPER_ADMIN (SaaS)).
  - `404 Not Found`: Si el recurso solicitado no existe.

## Estructura Técnica

### Request
```json
{
  "estado": 2
}
```

### Response (2xx)
```json
{
  "estado": "exito",
  "mensaje": "Estado de la empresa actualizado.",
  "datos": {
    "estado": 2
  }
}
```
