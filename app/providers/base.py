from pydantic import BaseModel
from typing import Optional

class CloudResource(BaseModel):
    provider: str
    name: str
    status: str
    server_type: Optional[str] = None
    region: Optional[str] = None
    public_ip: Optional[str] = None
    monthly_cost_usd: Optional[float] = None