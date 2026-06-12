# [METODO] /api/estado

## Historia de Usuario
> **Como** Público (Cualquier Actor)
> **Quiero** solicitar el Health Check del servidor matriz
> **Para** verificar que la API y la conexión a la base de datos están operativas para los balanceadores de carga.

## Criterios de Aceptación (Reglas de Negocio)
- Intenta realizar un `SELECT 1` a PostgreSQL. Si falla, el servicio se marca como Degraded.
- No requiere token de autenticación (Abierto al SRE/DevOps).
- **Códigos de Error:** 
  - `400 Bad Request`: Si los datos enviados no cumplen las validaciones.
  - `401 Unauthorized`: Si el token es inválido o no se envía.
  - `403 Forbidden`: Si el usuario no tiene los permisos (Público (Cualquier Actor)).
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
  "mensaje": "Servicio operativo",
  "datos": {
    "base_datos": "conectada"
  }
}
```
