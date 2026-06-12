# Canchita SaaS - Documentación Técnica (Por Endpoints y Roles)

## Arquitectura del Sistema
Canchita SaaS es una plataforma B2B2C (Business to Business to Consumer) diseñada para permitir que múltiples empresas administren y gestionen sus reservas de canchas deportivas utilizando una única infraestructura de base de datos compartida (arquitectura **Multi-Tenant con Schema Compartido**).

### Sistema de Roles (Niveles de Autorización)
Esta documentación está agrupada estrictamente por **Casos de Uso (Endpoints)** y separada por el **Rol** que tiene los privilegios para ejecutarlo. Los roles principales son:

1. **Público (Usuario No Autenticado):** Endpoints abiertos para creación de cuentas y peticiones de tokens.
2. **SUPER ADMIN (SaaS):** Dueños de la plataforma matriz. Capaces de suspender empresas (tenants) enteras o bloquear usuarios globales.
3. **Usuario Autenticado (Global):** Cualquier sesión viva en el sistema, capaz de cerrar su sesión o gestionar su perfil personal.

## Índice de Historias de Usuario (Por Módulo y Rol)

- [01. Autenticación](./modulos/autenticacion/)
  - **Público:** 
    - [Iniciar Sesión](./modulos/autenticacion/publico/post_iniciar_sesion.md)
    - [Registrar Cuenta](./modulos/autenticacion/publico/post_registrar_cuenta.md)
    - [Recuperar Clave](./modulos/autenticacion/publico/post_solicitar_recuperacion_clave.md)
    - [Restablecer Clave](./modulos/autenticacion/publico/post_restablecer_clave.md)
    - [Refrescar Token](./modulos/autenticacion/publico/post_refrescar_token.md)
  - **Usuario Autenticado:** 
    - [Cerrar Sesión](./modulos/autenticacion/usuario_autenticado/post_cerrar_sesion.md)
    - [Cerrar Sesión (Todos los dispositivos)](./modulos/autenticacion/usuario_autenticado/post_cerrar_sesion_todos.md)
- [02. Perfil de Usuario](./modulos/perfil_usuario/)
  - **Usuario Autenticado:** 
    - [Leer Perfil](./modulos/perfil_usuario/usuario_autenticado/get_perfil.md)
    - [Actualizar Perfil](./modulos/perfil_usuario/usuario_autenticado/put_perfil.md)
- [03. Gestión Global de Usuarios](./modulos/gestion_usuarios/)
  - **SUPER ADMIN:** 
    - [Listar Usuarios](./modulos/gestion_usuarios/super_admin/get_usuarios.md)
    - [Crear Usuario](./modulos/gestion_usuarios/super_admin/post_usuarios.md)
    - [Obtener Usuario por ID](./modulos/gestion_usuarios/super_admin/get_usuario_por_id.md)
    - [Actualizar Usuario](./modulos/gestion_usuarios/super_admin/put_usuario.md)
    - [Cambiar Estado (Bloquear)](./modulos/gestion_usuarios/super_admin/patch_estado_usuario.md)
    - [Eliminar Usuario](./modulos/gestion_usuarios/super_admin/delete_usuario.md)
- [04. Empresas SaaS (Tenants)](./modulos/saas_empresas/)
  - **SUPER ADMIN:** 
    - [Dar de alta empresa](./modulos/saas_empresas/super_admin/post_empresas.md)
    - [Listar empresas](./modulos/saas_empresas/super_admin/get_empresas.md)
    - [Detalle de empresa](./modulos/saas_empresas/super_admin/get_empresa_por_id.md)
    - [Actualizar empresa](./modulos/saas_empresas/super_admin/put_empresa.md)
    - [Suspender empresa](./modulos/saas_empresas/super_admin/patch_estado_empresa.md)
- [05. Monitoreo y Estado](./modulos/estado/)
  - **Público/DevOps:** 
    - [Ver estado general](./modulos/estado/publico/get_estado.md)
