# [METODO] /api/usuarios?pagina=1&tamano=10

## Historia de Usuario
> **Como** SUPER_ADMIN (SaaS)
> **Quiero** obtener una lista paginada de todos los usuarios registrados en toda la plataforma
> **Para** auditar el uso de la plataforma matriz, ver nuevos registros y aplicar filtros globales.

## Criterios de Aceptación (Reglas de Negocio)
- Si un `USUARIO_COMUN` intenta llamar a este endpoint, el Guardián de Roles Globales devuelve `403 Forbidden`.
- Soporta parámetros de búsqueda `?busqueda=juan` para filtrar por nombre o correo.
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
  "mensaje": "Usuarios obtenidos.",
  "datos": {
    "items": [...],
    "total": 500,
    "pagina": 1
  }
}
```
