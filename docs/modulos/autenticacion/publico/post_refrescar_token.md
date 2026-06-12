# [METODO] /api/autenticacion/refrescar-token

## Historia de Usuario
> **Como** Usuario con Token de Refresco
> **Quiero** intercambiar mi Token de Refresco vigente
> **Para** obtener un nuevo Token de Acceso sin tener que volver a escribir mi contraseña.

## Criterios de Aceptación (Reglas de Negocio)
- El token de refresco debe ser válido, no haber expirado, y no debe haber sido revocado en la base de datos.
- Una vez usado, opcionalmente el token de refresco antiguo puede invalidarse (Rotación de tokens).
- **Códigos de Error:** 
  - `400 Bad Request`: Si los datos enviados no cumplen las validaciones.
  - `401 Unauthorized`: Si el token es inválido o no se envía.
  - `403 Forbidden`: Si el usuario no tiene los permisos (Usuario con Token de Refresco).
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
  "mensaje": "Token renovado.",
  "datos": {
    "token_acceso": "eyJhbG..."
  }
}
```
