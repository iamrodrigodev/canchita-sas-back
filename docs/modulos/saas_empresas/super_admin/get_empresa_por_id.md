# [METODO] /api/saas/empresas/{empresa_id}

## Historia de Usuario
> **Como** SUPER_ADMIN (SaaS)
> **Quiero** solicitar los datos específicos tributarios y de configuración de una empresa cliente
> **Para** auditar los detalles de un cliente específico en la mesa de ayuda.

## Criterios de Aceptación (Reglas de Negocio)
- Retorna error 404 si la empresa no existe en el registro.
- Muestra información de auditoría como `fecha_creacion`.
- **Códigos de Error:** 
  - `400 Bad Request`: Si los datos enviados no cumplen las validaciones.
  - `401 Unauthorized`: Si el token es inválido o no se envía.
  - `403 Forbidden`: Si el usuario no tiene los permisos (SUPER_ADMIN (SaaS)).
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
  "mensaje": "Empresa obtenida.",
  "datos": {
    "id": 1,
    "nombre_comercial": "Canchas Pro"
  }
}
```
