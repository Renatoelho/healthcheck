from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/", status_code=200)
def get_example():
    return {"mensagem": "É um JSON de exemplo..."}

@app.get("/health", status_code=200)
def health_check():
    return {"status": "healthy"}
