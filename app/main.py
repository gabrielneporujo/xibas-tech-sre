import time
import logging
import json
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

# Configura logs estruturados em JSON
class JsonLogger(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
        })

handler = logging.StreamHandler()
handler.setFormatter(JsonLogger())
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)

# Cria a aplicação FastAPI
app = FastAPI(title="Xibas Tech SRE API")

# Ativa o endpoint /metrics automaticamente
Instrumentator().instrument(app).expose(app)

@app.get("/healthz")
def healthz():
    # Endpoint de health check — confirma que a API está viva
    logger.info("Health check chamado")
    return {"status": "ok"}

@app.get("/compute")
def compute(work: str = "500ms"):
    # Endpoint que simula carga — extrai o número de ms e dorme
    try:
        ms = int(work.replace("ms", ""))
    except ValueError:
        ms = 500
    logger.info(f"Simulando carga de {ms}ms")
    time.sleep(ms / 1000)
    return {"worked": f"{ms}ms"}