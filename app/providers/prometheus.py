import httpx
from app.config import settings

PROMETHEUS_API_BASE = f"{settings.prometheus_url}/api/v1/query"
CPU_USAGE_QUERY = '100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)'
CPU_USAGE_1H_QUERY = 'avg(rate(node_cpu_seconds_total{mode="idle"}[1h])) * 100'
RAM_USAGE_QUERY = '100 * (1 - ((node_memory_MemAvailable_bytes) / (node_memory_MemTotal_bytes)))'
DISK_USAGE_QUERY = '100 - ((node_filesystem_avail_bytes{mountpoint="/"} * 100) / node_filesystem_size_bytes{mountpoint="/"})'



async def fetch_prometheus_metrics(query: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PROMETHEUS_API_BASE}", params={"query": query})
        response.raise_for_status()
        return response.json()

async def fetch_cpu_usage() -> float  | None:
    data = await fetch_prometheus_metrics(CPU_USAGE_QUERY)
    results = data.get("data", {}).get("result", [])

    if not results:
        return None
    
    value = results[0]["value"][1]
    return round(float(value), 2)

async def fetch_cpu_usage_1h_avg() -> float | None:
    data = await fetch_prometheus_metrics(CPU_USAGE_1H_QUERY)
    results = data.get("data", {}).get("result", [])
    
    if not results:
        return None
    
    value = results[0]["value"][1]
    return round(float(value), 2)

async def fetch_ram_usage() -> float  | None:
    data = await fetch_prometheus_metrics(RAM_USAGE_QUERY)
    results = data.get("data", {}).get("result", [])

    if not results:
        return None
    
    value = results[0]["value"][1]
    return round(float(value), 2)

async def fetch_disk_usage() -> float | None:
    data = await fetch_prometheus_metrics(DISK_USAGE_QUERY)
    results = data.get("data", {}).get("result", [])

    if not results:
        return None

    value = results[0]["value"][1]
    return round(float(value), 2)