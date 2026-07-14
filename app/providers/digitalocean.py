import httpx
from app.config import settings


DIGITALOCEAN_API_BASE = "https://api.digitalocean.com/v2"

async def fetch_digitalocean_droplets():
    if not settings.digitalocean_api_token:
        return []
    
    headers = {"Authorization": f"Bearer {settings.digitalocean_api_token}"}

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(f"{DIGITALOCEAN_API_BASE}/droplets", headers=headers)
        response.raise_for_status()
        data = response.json()

    return data.get("droplets", [])
