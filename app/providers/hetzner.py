import httpx
from app.config import settings
from app.providers.base import CloudResource

HETZNER_API_BASE = "https://api.hetzner.cloud/v1"


async def fetch_hetzner_servers():
    if not settings.hetzner_api_token:
        return []
    
    headers = {"Authorization": f"Bearer {settings.hetzner_api_token}"}

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(f"{HETZNER_API_BASE}/servers", headers=headers)
        response.raise_for_status()
        data = response.json()

    raw_servers = data.get("servers", [])

    return [_to_cloud_resource(server) for server in raw_servers]

def _to_cloud_resource(server: dict) -> CloudResource:
    region_name = server.get("location", {}).get("name")
    prices = server.get("server_type", {}).get("prices", [])

    monthly_price = 0.0
    for price in prices:
        if price.get("location") == region_name:
            monthly_price = float(price.get("price_monthly", {}).get("net", 0.0))
            break

    if monthly_price == 0.0 and prices:
        monthly_price = float(prices[0].get("price_monthly", {}).get("net", 0.0))

    return CloudResource(
        provider="hetzner",
        name=server["name"],
        status=server["status"],
        server_type=server.get("server_type", {}).get("name"),
        region=region_name,  
        public_ip=server.get("public_net", {}).get("ipv4", {}).get("ip"),
        monthly_cost_usd=monthly_price
    )