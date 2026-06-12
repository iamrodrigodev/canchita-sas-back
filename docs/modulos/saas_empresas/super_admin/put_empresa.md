# [METODO] /api/saas/empresas/{empresa_id}

## Historia de Usuario
> **Como** SUPER_ADMIN (SaaS)
> **Quiero** modificar los datos comerciales o el subdominio asignado a un cliente
> **Para** actualizar la información tributaria si la empresa cambió de razón social o desea cambiar de subdominio web.

## Criterios de Aceptación (Reglas de Negocio)
- Valida que el nuevo subdominio no colisione con el de otro cliente existente.
- Actualiza la información en la tabla `empresas.empresas`.
- **Códigos de Error:** 
  - `400 Bad Request`: Si los datos enviados no cumplen las validaciones.
  - `401 Unauthorized`: Si el token es inválido o no se envía.
  - `403 Forbidden`: Si el usuario no tiene los permisos (SUPER_ADMIN (SaaS)).
  - `404 Not Found`: Si el recurso solicitado no existe.

## Estructura Técnica

### Request
```json
{
  "nombre_comercial": "Canchas Premium",
  "ruc": "10203040506",
  "subdominio": "premium"
}
```

### Response (2xx)
```json
{
  "estado": "exito",
  "mensaje": "Empresa actualizada.",
  "datos": {
    "id": 1
  }
}
```
