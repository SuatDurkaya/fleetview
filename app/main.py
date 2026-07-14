import asyncio
from fastapi import FastAPI
from app.config import settings
from app.providers.hetzner import fetch_hetzner_servers
from app.providers.digitalocean import fetch_digitalocean_droplets
from app.providers.aws import fetch_aws_instances

app = FastAPI()


@app.get("/")
def root():
    return {"status": "ok", "message": "Multi-Cloud Financial Solution is Working!"}

@app.get("/api/hetzner")
async def get_hetzner_servers():
    servers = await fetch_hetzner_servers()
    return {"servers": servers}

@app.get("/api/digitalocean")
async def get_digitalocean_droplets():
    droplets = await fetch_digitalocean_droplets()
    return {"droplets": droplets}

@app.get("/api/aws")
async def get_aws_instances():
    instances = await fetch_aws_instances()
    return {"instances": instances}

@app.get("/api/all")
async def get_all_resources():
    hetzner_task = fetch_hetzner_servers()
    digitalocean_task = fetch_digitalocean_droplets()
    aws_task = fetch_aws_instances()

    hetzner_servers, digitalocean_droplets, aws_instances = await asyncio.gather(hetzner_task, digitalocean_task, aws_task)

    return {
        "hetzner": {"servers": hetzner_servers},
        "digitalocean": {"droplets": digitalocean_droplets},
        "aws": {"instances": aws_instances}
    }