from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import asyncio

from app.config import settings
from app.providers.base import CloudResource 
from app.providers.hetzner import fetch_hetzner_servers
from app.providers.digitalocean import fetch_digitalocean_droplets
from app.providers.aws import fetch_aws_instances



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


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

@app.get("/api/resources", response_model=List[CloudResource])
async def get_resources():
    hetzner_task = fetch_hetzner_servers()
    digitalocean_task = fetch_digitalocean_droplets()
    aws_task = fetch_aws_instances()

    hetzner_servers, digitalocean_droplets, aws_instances = await asyncio.gather(
        hetzner_task, 
        digitalocean_task, 
        aws_task
    )

    all_resources = hetzner_servers + digitalocean_droplets + aws_instances
    return all_resources
    

