# [METODO] /api/autenticacion/solicitar-recuperacion-clave

## Historia de Usuario
> **Como** Usuario No Autenticado (Público)
> **Quiero** solicitar un enlace de recuperación proporcionando mi correo
> **Para** recibir las instrucciones para establecer una nueva contraseña si olvidé la actual.

## Criterios de Aceptación (Reglas de Negocio)
- Si el correo no existe en la BD, el sistema NO debe retornar 404, sino responder 200 genérico para evitar filtrado de correos válidos.
- El sistema genera un token OTP alfanumérico temporal válido por 30 minutos.
- **Códigos de Error:** 
  - `400 Bad Request`: Si los datos enviados no cumplen las validaciones.
  - `401 Unauthorized`: Si el token es inválido o no se envía.
  - `403 Forbidden`: Si el usuario no tiene los permisos (Usuario No Autenticado (Público)).
  - `404 Not Found`: Si el recurso solicitado no existe.

## Estructura Técnica

### Request
```json
{
  "correo": "juan@mail.com"
}
```

### Response (2xx)
```json
{
  "estado": "exito",
  "mensaje": "Si el correo existe, se enviarán instrucciones.",
  "datos": null
}
```
