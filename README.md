# Evite Problemas! Configure Health Checks no Docker de Forma Simples

Os **Health Checks** no Docker são fundamentais para garantir que sua aplicação esteja realmente funcionando dentro do contêiner. Muitas vezes, o fato de um contêiner estar ativo **não significa** que a aplicação está saudável. Para evitar problemas e melhorar o monitoramento, podemos configurar **Health Checks** no Docker Compose, permitindo que o próprio Docker verifique periodicamente o status da aplicação.

Neste guia, você aprenderá como implementar Health Checks de maneira simples utilizando **FastAPI** e **Docker Compose**, garantindo que seus serviços estejam sempre monitorados e prontos para uso.

## Apresentação em Vídeo

<p align="center">
  <a href="https://youtu.be/X6Nerb-3_R0" target="_blank"><img src="imagens/thumbnail/thumbnail-health-check-docker-github-01.png" alt="Vídeo de apresentação"></a>
</p>

![YouTube Video Views](https://img.shields.io/youtube/views/X6Nerb-3_R0) ![YouTube Video Likes](https://img.shields.io/youtube/likes/X6Nerb-3_R0)

### Requisitos

+ ![Docker](https://img.shields.io/badge/Docker-27.4.1-E3E3E3)
+ ![Docker-compose](https://img.shields.io/badge/Docker--compose-1.25.0-E3E3E3)
+ ![Git](https://img.shields.io/badge/Git-2.25.1%2B-E3E3E3)
+ ![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04%2B-E3E3E3)

## O que são Health Checks?

O **Health Check** é um mecanismo que permite ao Docker verificar periodicamente se um contêiner está funcionando corretamente. Ele é configurado dentro do **Docker Compose** e pode executar comandos para testar se a aplicação está respondendo de maneira adequada.

📌 **Exemplo de Health Check:**
- Verificar se uma API responde com **status 200**.
- Checar se um banco de dados está acessível.
- Monitorar serviços internos essenciais da aplicação.

## Implementando um Health Check no Docker

### Criando um Endpoint de Verificação

Primeiramente, vamos criar uma API utilizando **FastAPI** e adicionar um endpoint chamado `/health`, que responderá **200 OK** quando tudo estiver funcionando.

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/", status_code=200)
def get_example():
    return {"mensagem": "É um JSON de exemplo..."}

@app.get("/health", status_code=200)
def health_check():
    return {"status": "healthy"}
```

Esse endpoint será utilizado pelo Docker para verificar se a aplicação está ativa.

### Configurando o Health Check no Docker Compose

Agora, adicionamos o **Health Check** ao nosso `docker-compose.yml`:

```yaml
services:
  api-teste:
    container_name: api-teste
    hostname: api-teste
    image: python:3.12-slim
    ports:
      - "8000:8000"
    volumes:
      - ./src:/src
    working_dir: /src
    command: >
      sh -c "apt update && apt install curl -y && pip install -U pip && pip install fastapi==0.115.5 uvicorn==0.32.0 && uvicorn app:app --host 0.0.0.0 --port 8000"
    healthcheck:
      test: curl -f http://localhost:8000/health
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 5s
```

📌 **Explicação dos parâmetros:**
- `test`: Executa um comando para verificar o endpoint `/health`.
- `interval`: Define o intervalo entre as verificações (30 segundos).
- `timeout`: Define o tempo limite para considerar a resposta válida (10 segundos).
- `retries`: Número de tentativas antes de marcar como **"unhealthy"**.
- `start_period`: Tempo de espera antes de iniciar as verificações (5 segundos).

## Testando o Health Check

Após configurar o **Docker Compose**, subimos a aplicação e verificamos seu status:

```bash
docker compose -p healthcheck -f docker-compose.yaml up -d
```

Para checar se o Health Check está funcionando:

```bash
docker ps
```

Caso o contêiner esteja saudável, o status será exibido como **healthy**. Se houver falha, ele será marcado como **unhealthy**, indicando que a aplicação não está respondendo corretamente.

## Melhorando a Visualização do Status

Podemos criar um **alias** para simplificar a exibição do status dos contêineres:

```bash
echo "alias dockerps='docker ps --format '{{.ID}}\t{{.Names}}\t{{.Status}}''" >> ~/.bashrc

source ~/.bashrc
```

Agora, basta rodar o comando `dockerps` para visualizar somente o **ID**, **Nome** e **Status** dos contêineres de forma organizada.

## Referências

HEALTHCHECK, **Docker Docs**. Disponível em: <https://docs.docker.com/engine/reference/builder/#healthcheck>. Acesso em: 28 fev. 2025.

FastAPI, **Documentação Oficial**. Disponível em: <https://fastapi.tiangolo.com/>. Acesso em: 28 fev. 2025.

