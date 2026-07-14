import httpx
import asyncio
import boto3
from app.config import settings


def _fetch_sync():
    client = boto3.client(
        "ec2",
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        region_name=settings.aws_region,
    )
    response = client.describe_instances()

    instances = []
    for reservation in response.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            instances.append(instance)
    
    return instances

async def fetch_aws_instances():
    if not settings.aws_access_key_id or not settings.aws_secret_access_key:
        return []
        
    return await asyncio.to_thread(_fetch_sync)
    
