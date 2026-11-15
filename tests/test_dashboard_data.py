from dashboard.api_client import mock_dashboard_data


def test_mock_data_has_expected_sections():
    summary, resources, recommendations, anomalies, forecast = mock_dashboard_data()
    assert summary["total_resources"] == len(resources)
    assert summary["total_monthly_expenditure"] > 0
    assert resources
    assert recommendations
    assert anomalies
    assert len(forecast) == 7


def test_mock_savings_matches_recommendations():
    summary, _, recommendations, _, _ = mock_dashboard_data()
    calculated = sum(float(item["estimated_savings"]) for item in recommendations)
    assert round(calculated, 2) == summary["estimated_potential_savings"]
