
from datetime import date, timedelta


# CLOUDLEAK DEMO DATA
# These records are simulated for independent backend development.
# They will be replaced with the actual collector data during integration.

MOCK_RESOURCES = [
    {
        "resource_id": "EC2-001",
        "resource_type": "EC2",
        "region": "us-east-1",
        "usage": 720.0,
        "cost": 145.50,
        "utilization": 28.0
    },
    {
        "resource_id": "EC2-002",
        "resource_type": "EC2",
        "region": "us-west-2",
        "usage": 680.0,
        "cost": 210.00,
        "utilization": 82.0
    },
    {
        "resource_id": "RDS-001",
        "resource_type": "RDS",
        "region": "us-east-1",
        "usage": 500.0,
        "cost": 185.75,
        "utilization": 35.0
    },
    {
        "resource_id": "S3-001",
        "resource_type": "S3",
        "region": "ap-south-1",
        "usage": 1200.0,
        "cost": 42.25,
        "utilization": 65.0
    },
    {
        "resource_id": "EC2-003",
        "resource_type": "EC2",
        "region": "ap-south-1",
        "usage": 800.0,
        "cost": 320.00,
        "utilization": 92.0
    }
]


def get_resources():
    """Return simulated cloud resource records."""
    return [resource.copy() for resource in MOCK_RESOURCES]


def get_total_cost():
    """Calculate total simulated cloud expenditure."""
    return round(sum(item["cost"] for item in MOCK_RESOURCES), 2)


def get_resource_count():
    """Return the number of simulated cloud resources."""
    return len(MOCK_RESOURCES)


def get_average_cost():
    """Calculate average cost per resource."""
    count = get_resource_count()

    if count == 0:
        return 0.0

    return round(get_total_cost() / count, 2)


def get_cost_breakdown(field):
    """Group resource costs by service type or region."""
    breakdown = {}

    for resource in MOCK_RESOURCES:
        key = resource[field]
        breakdown[key] = breakdown.get(key, 0.0) + resource["cost"]

    return [
        {"name": name, "cost": round(cost, 2)}
        for name, cost in sorted(breakdown.items())
    ]


def get_mock_anomalies():
    """Return simulated cost anomalies."""
    today = date.today()

    return [
        {
            "resource_id": "EC2-003",
            "date": today.isoformat(),
            "observed_cost": 320.00,
            "expected_cost": 210.00,
            "deviation_percentage": 52.38,
            "severity": "high"
        },
        {
            "resource_id": "RDS-001",
            "date": (today - timedelta(days=1)).isoformat(),
            "observed_cost": 185.75,
            "expected_cost": 150.00,
            "deviation_percentage": 23.83,
            "severity": "medium"
        }
    ]
