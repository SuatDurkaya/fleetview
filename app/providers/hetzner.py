import httpx
from app.config import settings

HETZNER_API_BASE = "https://api.hetzner.cloud/v1"


async def fetch_hetzner_servers():
    if not settings.hetzner_api_token:
        return []
    
    headers = {"Authorization": f"Bearer {settings.hetzner_api_token}"}

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(f"{HETZNER_API_BASE}/servers", headers=headers)
        response.raise_for_status()
        data = response.json()

    return data.get("servers", [])