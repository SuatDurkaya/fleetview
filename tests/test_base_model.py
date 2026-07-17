from app.providers.base import CloudResource
import pytest
from pydantic import ValidationError

def test_cloud_resource_accepts_all_data():
    resource = CloudResource(
        provider="Hetzner",
        name="Test-Instance",
        status="running",
        server_type="cx31",
        region="fsn1",
        public_ip="1.2.3.4",
        monthly_cost_usd=5.0
    )

    assert resource.provider == "Hetzner"
    assert resource.name == "Test-Instance"
    assert resource.monthly_cost_usd == 5.0


def test_cloud_resource_optional_fields():
    resource = CloudResource(
        provider="aws",
        name="Test-Instance",
        status="active"
    )

    assert resource.server_type is None
    assert resource.public_ip is None
    assert resource.monthly_cost_usd is None

def test_cloud_resource_obligates_provider_name_status():
    with pytest.raises(ValidationError):
        CloudResource(
            provider="hetzner",
            status="running"  # there are not name variable.
        )