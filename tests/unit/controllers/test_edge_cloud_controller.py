import pytest
from unittest.mock import MagicMock, patch
from flask import Flask
from edge_cloud_management_api.controllers.edge_cloud_controller import (
    get_edge_cloud_zones,
)
from edge_cloud_management_api.app import get_app_instance

MOCK_ZONES = [
    {
        "edgeCloudZoneId": "046b6c7f-0b8a-43b9-b35d-6489e6daee91",
        "edgeCloudZoneName": "Zone1",
        "edgeCloudZoneStatus": "active",
        "edgeCloudProvider": "Provider1",
        "edgeCloudRegion": "Region1",
    },
    {
        "edgeCloudZoneId": "513e4567-e89b-12d3-a456-426614174000",
        "edgeCloudZoneName": "Zone3",
        "edgeCloudZoneStatus": "inactive",
        "edgeCloudProvider": "Provider3",
        "edgeCloudRegion": "Region1",
    },
    {
        "edgeCloudZoneId": "123e4567-e89b-12d3-a456-426614174000",
        "edgeCloudZoneName": "Zone2",
        "edgeCloudZoneStatus": "inactive",
        "edgeCloudProvider": "Provider2",
        "edgeCloudRegion": "Region2",
    },
]


@pytest.fixture
def test_app():
    flask_app = get_app_instance()
    return flask_app.app


@pytest.fixture
def mock_get_all_cloud_zones():
    with patch(
        "edge_cloud_management_api.controllers.edge_cloud_controller.get_all_cloud_zones",
        return_value=MOCK_ZONES,
    ) as mock_function:
        yield mock_function


@pytest.mark.parametrize(
    "x_correlator, region, status, expected_response_status, expected_count",
    [
        (None, None, None, 200, 3),  # No filters, return all
        (None, "Region2", None, 200, 1),  # Filter by region
        (None, None, "inactive", 200, 2),  # Filter by inactive status
        (None, None, "active", 200, 1),  # Filter by active status
        (None, "Region1", "active", 200, 1),  # Filter by region and status
        (None, "Region3", None, 200, 0),  # Region not in data
        (None, None, "invalid", 400, 0),  # invalid status
    ],
)
def test_get_edge_cloud_zones(
    x_correlator,
    region,
    status,
    expected_response_status,
    expected_count,
    mock_get_all_cloud_zones: MagicMock,
    test_app: Flask,
):
    """
    Test the get_edge_cloud_zones controller.
    """
    with test_app.test_request_context():
        response, response_status = get_edge_cloud_zones(x_correlator, region, status)
        assert response_status == expected_response_status
        if expected_response_status == 400:
            assert response.json["code"] == "VALIDATION_ERROR"
        elif expected_response_status == 200:
            assert len(response.json) == expected_count
            mock_get_all_cloud_zones.assert_called_once()
        else:
            assert False
