# [METODO] /api/autenticacion/registrar-cuenta

## Historia de Usuario
> **Como** Usuario No Autenticado (Público)
> **Quiero** registrarme en la plataforma creando una cuenta con mis datos personales
> **Para** poder iniciar sesión posteriormente y acceder a las funcionalidades del sistema.

## Criterios de Aceptación (Reglas de Negocio)
- El sistema debe validar que el correo electrónico no esté registrado previamente.
- La contraseña enviada será cifrada unidireccionalmente (Bcrypt) antes de guardarse.
- **Códigos de Error:** 
  - `400 Bad Request`: Si los datos enviados no cumplen las validaciones.
  - `401 Unauthorized`: Si el token es inválido o no se envía.
  - `403 Forbidden`: Si el usuario no tiene los permisos (Usuario No Autenticado (Público)).
  - `404 Not Found`: Si el recurso solicitado no existe.

## Estructura Técnica

### Request
```json
{
  "nombre": "Juan",
  "apellidos": "Perez",
  "correo": "juan@mail.com",
  "clave": "Segura123!",
  "telefono": "999888777"
}
```

### Response (2xx)
```json
{
  "estado": "exito",
  "mensaje": "Cuenta creada exitosamente.",
  "datos": {
    "id": 10,
    "correo": "juan@mail.com"
  }
}
```
