
from backend.services.data_service import (
    get_resources,
    get_total_cost,
    get_resource_count,
    get_average_cost,
    get_cost_breakdown
)


def test_get_resources():
    resources = get_resources()

    assert isinstance(resources, list)
    assert len(resources) == 5


def test_get_total_cost():
    total = get_total_cost()

    assert total == 903.50


def test_get_resource_count():
    assert get_resource_count() == 5


def test_get_average_cost():
    assert get_average_cost() == 180.70


def test_service_cost_breakdown():
    breakdown = get_cost_breakdown("resource_type")

    assert isinstance(breakdown, list)
    assert len(breakdown) == 3

    for item in breakdown:
        assert "name" in item
        assert "cost" in item


def test_get_resources_returns_independent_data():
    first_result = get_resources()

    first_result[0]["cost"] = 999999

    second_result = get_resources()

    assert second_result[0]["cost"] != 999999
