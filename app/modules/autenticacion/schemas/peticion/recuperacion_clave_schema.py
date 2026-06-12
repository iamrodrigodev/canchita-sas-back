from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError
from app.core.security.validador_claves import ValidadorClaves


class SolicitarRecuperacionClavePeticion(BaseModel):
    correo: str = Field(...)

    @field_validator('correo')
    @classmethod
    def validar_correo(cls, v):
        if not v or len(v.strip()) == 0:
            raise PydanticCustomError('value_error', 'El correo es obligatorio')
        return v.strip().lower()


class RestablecerClavePeticion(BaseModel):
    token_recuperacion: str = Field(..., min_length=20)
    nueva_clave: str = Field(..., min_length=6, max_length=255)

    @field_validator('token_recuperacion')
    @classmethod
    def validar_token(cls, v):
        if not v or len(v.strip()) == 0:
            raise PydanticCustomError('value_error', 'El token de recuperacion es obligatorio')
        return v.strip()

    @field_validator('nueva_clave')
    @classmethod
    def validar_clave(cls, v):
        return ValidadorClaves.validar_fortaleza(v)
