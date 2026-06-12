# [METODO] /api/usuarios/{usuario_id}

## Historia de Usuario
> **Como** SUPER_ADMIN (SaaS)
> **Quiero** sobrescribir los datos de la cuenta de cualquier usuario de forma administrativa
> **Para** corregir errores manuales, modificar correos o hacer actualizaciones que el usuario por sí solo no pueda.

## Criterios de Aceptación (Reglas de Negocio)
- Se ignorará la actualización si el nuevo correo enviado ya le pertenece a una tercera cuenta.
- Requiere rol SUPER_ADMIN.
- **Códigos de Error:** 
  - `400 Bad Request`: Si los datos enviados no cumplen las validaciones.
  - `401 Unauthorized`: Si el token es inválido o no se envía.
  - `403 Forbidden`: Si el usuario no tiene los permisos (SUPER_ADMIN (SaaS)).
  - `404 Not Found`: Si el recurso solicitado no existe.

## Estructura Técnica

### Request
```json
{
  "nombre": "Juan Corregido",
  "rol_id": 2,
  "estado": 1
}
```

### Response (2xx)
```json
{
  "estado": "exito",
  "mensaje": "Usuario actualizado.",
  "datos": {
    "id": 5
  }
}
```
