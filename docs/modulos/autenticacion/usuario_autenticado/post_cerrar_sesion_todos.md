# [METODO] /api/autenticacion/cerrar-sesion-todos

## Historia de Usuario
> **Como** Usuario Autenticado (Cualquier Rol)
> **Quiero** ejecutar un cierre de sesión global
> **Para** revocar todos los tokens de refresco activos asociados a mi cuenta en todos los dispositivos.

## Criterios de Aceptación (Reglas de Negocio)
- El sistema ejecuta un UPDATE masivo marcando `revocado = true` a todos los tokens activos del usuario solicitante.
- Esto fuerza el cierre de sesión en celulares, navegadores web y tablets simultáneamente.
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
  "mensaje": "Todas las sesiones fueron cerradas.",
  "datos": null
}
```
