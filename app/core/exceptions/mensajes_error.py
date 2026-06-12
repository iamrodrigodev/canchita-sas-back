from enum import Enum


class MensajesDeError(Enum):
    DATOS_INVALIDOS = ("Datos de entrada invalidos", 400)
    USUARIO_NO_ENCONTRADO = ("El usuario no existe", 404)
    CREDENCIALES_INVALIDAS = ("Credenciales incorrectas", 401)
    CUENTA_BLOQUEADA = ("Cuenta bloqueada", 403)
    EMAIL_DUPLICADO = ("El correo electronico ya esta registrado", 400)
    ERROR_INTERNO = ("Error interno del servidor", 500)
    ACCESO_DENEGADO = ("Acceso denegado", 403)
    NO_AUTORIZADO = ("No autorizado", 401)
    RECURSO_NO_ENCONTRADO = ("Recurso no encontrado", 404)
    TOKEN_RECUPERACION_INVALIDO = ("Token de recuperacion invalido o expirado", 400)
    ROL_NO_EXISTE = ("El rol indicado no existe", 400)
    PAGINACION_INVALIDA = ("La pagina debe ser mayor o igual a 1", 400)
    TAMANO_PAGINA_INVALIDO = ("El tamano debe estar entre 1 y 100", 400)
    ESTADO_INVALIDO = ("El estado debe ser 0 o 1", 400)
    NO_PUEDE_AUTODESACTIVARSE = ("No puede desactivar su propio usuario", 400)

    def __init__(self, mensaje, codigo):
        self.mensaje = mensaje
        self.codigo = codigo
