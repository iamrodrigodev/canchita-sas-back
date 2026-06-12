import logging

from app.core.config.metricas import auditoria_backend
from app.utils.datos_sensibles import sanitizar_campos_sensibles

logger = logging.getLogger("fastapi")


def registrar_evento_auditoria(evento: str, resultado: str, **campos):
    campos = sanitizar_campos_sensibles(campos)
    partes = [f"evento={evento}", f"resultado={resultado}"]
    for clave, valor in campos.items():
        partes.append(f"{clave}={valor}")
    logger.info("[AUDITORIA] " + " ".join(partes))
    auditoria_backend.registrar(evento, resultado, campos)
