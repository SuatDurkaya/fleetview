from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from fastapi.responses import FileResponse
from pydantic import BaseModel
import asyncio

from app.auth import verify_password, create_access_token, verify_token
from app.config import settings
from app.providers.base import CloudResource 
from app.providers.hetzner import fetch_hetzner_servers
from app.providers.digitalocean import fetch_digitalocean_droplets
from app.providers.aws import fetch_aws_instances
from app.providers.prometheus import fetch_cpu_usage, fetch_ram_usage, fetch_disk_usage, fetch_cpu_usage_1h_avg





class LoginRequest(BaseModel):
    password: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.post("/api/login")
async def login(credentials: LoginRequest):
    if not verify_password(credentials.password):
        raise HTTPException(status_code=401, detail="Şifre yanlış")

    token = create_access_token()
    return {"access_token": token, "token_type": "bearer"}

@app.get("/api/hetzner", dependencies=[Depends(verify_token)])
async def get_hetzner_servers():
    servers = await fetch_hetzner_servers()
    return {"servers": servers}

@app.get("/api/digitalocean", dependencies=[Depends(verify_token)])
async def get_digitalocean_droplets():
    droplets = await fetch_digitalocean_droplets()
    return {"droplets": droplets}

@app.get("/api/aws", dependencies=[Depends(verify_token)])
async def get_aws_instances():
    instances = await fetch_aws_instances()
    return {"instances": instances}

@app.get("/api/resources", response_model=List[CloudResource], dependencies=[Depends(verify_token)])
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
    
@app.get("/api/metrics", dependencies=[Depends(verify_token)])
async def get_metrics():
    cpu, ram, disk, cpu_1h_avg = await asyncio.gather(
        fetch_cpu_usage(),
        fetch_ram_usage(),
        fetch_disk_usage(),
        fetch_cpu_usage_1h_avg(),
    )

    is_idle = (
        cpu_1h_avg is not None and cpu_1h_avg < settings.idle_cpu_threshold_percent
    )
    return {
        "cpu_usage_percent": cpu,
        "ram_usage_percent": ram,
        "disk_usage_percent": disk,
        "cpu_usage_1h_avg_percent": cpu_1h_avg,
        "is_idle": is_idle,
    }