import re
from pydantic_core import PydanticCustomError

class ValidadorClaves:
    @staticmethod
    def validar_fortaleza(clave: str) -> str:
        if not clave:
            raise PydanticCustomError('value_error', 'La clave no puede estar vacía')
            
        if len(clave) < 8:
            raise PydanticCustomError('value_error', 'La clave debe tener al menos 8 caracteres')
            
        if not re.search(r"[A-Z]", clave):
            raise PydanticCustomError('value_error', 'La clave debe contener al menos una letra mayúscula')
            
        if not re.search(r"[a-z]", clave):
            raise PydanticCustomError('value_error', 'La clave debe contener al menos una letra minúscula')
            
        if not re.search(r"\d", clave):
            raise PydanticCustomError('value_error', 'La clave debe contener al menos un número')
            
        if not re.search(r"[\W_]", clave):
            raise PydanticCustomError('value_error', 'La clave debe contener al menos un carácter especial (ej. @, #, $, %, etc.)')
            
        return clave
