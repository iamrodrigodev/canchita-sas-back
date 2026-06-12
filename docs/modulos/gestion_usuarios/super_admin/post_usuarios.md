# [METODO] /api/usuarios

## Historia de Usuario
> **Como** SUPER_ADMIN (SaaS)
> **Quiero** crear manualmente la cuenta de un nuevo usuario en la base de datos matriz
> **Para** dar de alta un usuario saltándose el proceso de registro público (ej. creación de otro Super Admin o Soporte).

## Criterios de Aceptación (Reglas de Negocio)
- El correo proporcionado no debe existir en la base de datos.
- Permite asignar el `rol_id` directamente (ej. crear un SUPER_ADMIN), cosa que el registro público no permite.
- **Códigos de Error:** 
  - `400 Bad Request`: Si los datos enviados no cumplen las validaciones.
  - `401 Unauthorized`: Si el token es inválido o no se envía.
  - `403 Forbidden`: Si el usuario no tiene los permisos (SUPER_ADMIN (SaaS)).
  - `404 Not Found`: Si el recurso solicitado no existe.

## Estructura Técnica

### Request
```json
{
  "nombre": "Soporte",
  "apellidos": "Tecnico",
  "correo": "soporte@saas.com",
  "clave": "ClaveFuerte1!",
  "rol_id": 1
}
```

### Response (2xx)
```json
{
  "estado": "exito",
  "mensaje": "Usuario creado.",
  "datos": {
    "id": 2
  }
}
```
