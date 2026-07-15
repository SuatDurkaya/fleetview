import httpx
from app.config import settings

PROMETHEUS_API_BASE = f"{settings.prometheus_url}/api/v1/query"
CPU_USAGE_QUERY = '100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)'

async def fetch_prometheus_metrics(cpu_query: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PROMETHEUS_API_BASE}", params={"query": cpu_query})
        response.raise_for_status()
        return response.json()

async def fetch_cpu_usage() -> float  | None:
    data = await fetch_prometheus_metrics(CPU_USAGE_QUERY)
    results = data.get("data", {}).get("result", [])

    if not results:
        return None
    
    value = results[0]["value"][1]
    return round(float(value), 2)