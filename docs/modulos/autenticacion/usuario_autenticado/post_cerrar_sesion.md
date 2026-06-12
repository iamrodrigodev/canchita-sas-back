# [METODO] /api/autenticacion/cerrar-sesion

## Historia de Usuario
> **Como** Usuario Autenticado (Cualquier Rol)
> **Quiero** enviar una petición para cerrar mi sesión actual
> **Para** revocar mi Token de Refresco actual en la base de datos para impedir que siga generando nuevos accesos.

## Criterios de Aceptación (Reglas de Negocio)
- El sistema buscará el token de refresco provisto y lo marcará como `revocado = true`.
- El JWT Access Token del lado del cliente debe ser borrado por el frontend (LocalStorage/Cookies).
- **Códigos de Error:** 
  - `400 Bad Request`: Si los datos enviados no cumplen las validaciones.
  - `401 Unauthorized`: Si el token es inválido o no se envía.
  - `403 Forbidden`: Si el usuario no tiene los permisos (Usuario Autenticado (Cualquier Rol)).
  - `404 Not Found`: Si el recurso solicitado no existe.

## Estructura Técnica

### Request
```json
{
  "token_refresco": "eyJhbG..."
}
```

### Response (2xx)
```json
{
  "estado": "exito",
  "mensaje": "Sesión cerrada.",
  "datos": null
}
```
