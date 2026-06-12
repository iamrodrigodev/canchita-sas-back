# [METODO] /api/saas/empresas

## Historia de Usuario
> **Como** SUPER_ADMIN (SaaS)
> **Quiero** obtener el listado de todas las empresas (tenants) dadas de alta en la plataforma
> **Para** gestionar y monitorear la cartera total de clientes corporativos del SaaS.

## Criterios de Aceptación (Reglas de Negocio)
- Puede filtrar por estado (Activas, Suspendidas).
- Requiere rol SUPER_ADMIN. Si accede un cliente de una empresa, le retornará 403 Forbidden.
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
  "mensaje": "Empresas listadas.",
  "datos": {
    "items": [...],
    "total": 10
  }
}
```
