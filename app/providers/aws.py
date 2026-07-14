import httpx
import asyncio
import boto3
from app.config import settings
from app.providers.base import CloudResource

AWS_EC2_PRICES = {
    "t2.nano": 4.20,
    "t2.micro": 8.50,
    "t2.small": 17.00,
    "t2.medium": 34.00,
    "t3.nano": 3.80,
    "t3.micro": 7.60,
    "t3.small": 15.20,
    "t3.medium": 30.40,
    "t3.large": 60.80,
    "m5.large": 70.00,
    "t4g.nano": 3.00,
    "t4g.micro": 6.10,
    "t4g.small": 12.20,
    "t4g.medium": 24.40,
}

def _to_cloud_resource(instance: dict) -> CloudResource:
    instance_name = instance.get("InstanceId")
    for tag in instance.get("Tags", []):
        if tag.get("Key") == "Name":
            instance_name = tag.get("Value")
            break
    
    az_name = instance.get("Placement", {}).get("AvailabilityZone")
    instance_type = instance.get("InstanceType")
    monthly_cost = AWS_EC2_PRICES.get(instance_type, 0.0) # AWS does not provide direct monthly cost in the API response

    return CloudResource(
        provider="aws",
        name=instance_name,
        status=instance.get("State", {}).get("Name"),
        server_type=instance.get("InstanceType"),
        region=az_name,
        public_ip=instance.get("PublicIpAddress"),
        monthly_cost_usd=monthly_cost
    )


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

    raw_instances = await asyncio.to_thread(_fetch_sync)
        
    return [_to_cloud_resource(instance) for instance in raw_instances]
    
