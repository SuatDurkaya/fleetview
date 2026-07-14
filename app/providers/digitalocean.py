import httpx
from app.config import settings
from app.providers.base import CloudResource

DIGITALOCEAN_API_BASE = "https://api.digitalocean.com/v2"

async def fetch_digitalocean_droplets():
    if not settings.digitalocean_api_token:
        return []
    
    headers = {"Authorization": f"Bearer {settings.digitalocean_api_token}"}

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(f"{DIGITALOCEAN_API_BASE}/droplets", headers=headers)
        response.raise_for_status()
        data = response.json()

    return [(_to_cloud_resource(droplet)) for droplet in data.get("droplets", [])]

def _to_cloud_resource(droplet: dict) -> CloudResource:
    networks = droplet.get("networks", {}).get("v4", [])
    public_ip = None
    for net in networks:
        if net.get("type") == "public":
            public_ip = net.get("ip_address")
            break

    monthly_cost = float(droplet.get("size", {}).get("price_monthly", 0.0))


    return CloudResource(
        provider="digitalocean",
        name=droplet["name"],
        status=droplet["status"],
        server_type=droplet.get("size_slug"),
        region=droplet.get("region", {}).get("name"),
        public_ip=public_ip,
        monthly_cost_usd=monthly_cost
    )