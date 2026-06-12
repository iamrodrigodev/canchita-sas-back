from starlette.middleware.base import BaseHTTPMiddleware
import time
from collections import defaultdict
from statistics import mean

class RegistroMetricas:
    def __init__(self):
        self.conteo_estado = defaultdict(int)
        self.latencias = defaultdict(list)

    def registrar(self, ruta: str, metodo: str, estado: int, duracion_ms: float):
        clave = f"{metodo} {ruta}"
        self.conteo_estado[f"{clave}:{estado}"] += 1
        lista = self.latencias[clave]
        lista.append(duracion_ms)
        if len(lista) > 1000:
            del lista[:200]

    def snapshot(self):
        resumen = {}
        for clave, lista in self.latencias.items():
            ordenadas = sorted(lista)
            p95_idx = max(0, int(len(ordenadas) * 0.95) - 1)
            resumen[clave] = {
                "count": len(lista),
                "promedio_ms": round(mean(lista), 2),
                "p95_ms": round(ordenadas[p95_idx], 2),
            }
        return {
            "latencias": resumen,
            "conteo_estado": dict(self.conteo_estado),
        }

metricas_backend = RegistroMetricas()


class RegistroAuditoria:
    def __init__(self):
        self.conteo_eventos = defaultdict(int)
        self.ultimos_eventos = []

    def registrar(self, evento: str, resultado: str, campos: dict):
        clave = f"{evento}:{resultado}"
        self.conteo_eventos[clave] += 1
        self.ultimos_eventos.append(
            {
                "evento": evento,
                "resultado": resultado,
                "campos": campos,
            }
        )
        if len(self.ultimos_eventos) > 300:
            del self.ultimos_eventos[:100]

    def snapshot(self):
        return {
            "conteo_eventos": dict(self.conteo_eventos),
            "ultimos_eventos": list(self.ultimos_eventos[-50:]),
        }


auditoria_backend = RegistroAuditoria()

class MiddlewareMetricas(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        inicio = time.perf_counter()
        response = await call_next(request)
        fin = time.perf_counter()
        metricas_backend.registrar(request.url.path, request.method, response.status_code, (fin - inicio) * 1000)
        return response


