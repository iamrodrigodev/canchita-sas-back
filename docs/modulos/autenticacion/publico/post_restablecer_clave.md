# [METODO] /api/autenticacion/restablecer-clave

## Historia de Usuario
> **Como** Usuario No Autenticado (Público)
> **Quiero** enviar mi token de recuperación junto con una nueva clave segura
> **Para** actualizar mi contraseña en la base de datos y poder iniciar sesión.

## Criterios de Aceptación (Reglas de Negocio)
- El token debe existir en `tokens_recuperacion_clave` y no debe haber sido marcado como usado.
- Al tener éxito, el token se marca como `usado = true` para evitar ataques de repetición.
- **Códigos de Error:** 
  - `400 Bad Request`: Si los datos enviados no cumplen las validaciones.
  - `401 Unauthorized`: Si el token es inválido o no se envía.
  - `403 Forbidden`: Si el usuario no tiene los permisos (Usuario No Autenticado (Público)).
  - `404 Not Found`: Si el recurso solicitado no existe.

## Estructura Técnica

### Request
```json
{
  "token": "ABC123XYZ",
  "nueva_clave": "NuevaSuperClave123!"
}
```

### Response (2xx)
```json
{
  "estado": "exito",
  "mensaje": "Contraseña restablecida exitosamente.",
  "datos": null
}
```
