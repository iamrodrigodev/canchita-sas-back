# [METODO] /api/saas/empresas

## Historia de Usuario
> **Como** SUPER_ADMIN (SaaS)
> **Quiero** registrar los datos de un nuevo cliente corporativo (Empresa) en el sistema multi-tenant
> **Para** abrir un nuevo espacio de trabajo aislado (tenant) para que esta empresa pueda usar el software.

## Criterios de Aceptación (Reglas de Negocio)
- El campo `subdominio` o `ruc` no debe estar repetido a nivel nacional en la base de datos.
- Asigna automáticamente a `usuario_dueño_id` como el propietario/administrador de esa nueva empresa.
- **Códigos de Error:** 
  - `400 Bad Request`: Si los datos enviados no cumplen las validaciones.
  - `401 Unauthorized`: Si el token es inválido o no se envía.
  - `403 Forbidden`: Si el usuario no tiene los permisos (SUPER_ADMIN (SaaS)).
  - `404 Not Found`: Si el recurso solicitado no existe.

## Estructura Técnica

### Request
```json
{
  "nombre_comercial": "Canchas Pro",
  "ruc": "10203040506",
  "subdominio": "canchaspro",
  "usuario_dueño_id": 2
}
```

### Response (2xx)
```json
{
  "estado": "exito",
  "mensaje": "Empresa creada.",
  "datos": {
    "id": 1
  }
}
```
