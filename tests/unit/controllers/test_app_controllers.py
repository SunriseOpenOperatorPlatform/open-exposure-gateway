import pytest
from unittest.mock import MagicMock, patch
from flask import Flask
from edge_cloud_management_api.app import get_app_instance
from edge_cloud_management_api.controllers.app_controllers import submit_app, get_app


@pytest.fixture
def test_app():
    """Get the Flask app instance.
    This fixture allows us to test the controllers,
    including the request context as it would be in a real HTTP request.
    """
    flask_app = get_app_instance()
    return flask_app.app


@pytest.mark.parametrize(
    "app_id, x_correlator, expected",
    [
        (1, None, "do some magic!"),
        (2, "123", "do some magic!"),
    ],
)
def test_get_app(app_id, x_correlator, expected):
    """
    Test the get_app controller.
    """
    result = get_app(app_id, x_correlator)
    assert result == expected


@pytest.fixture
def mock_get_all_cloud_zones():
    with patch(
        "edge_cloud_management_api.controllers.edge_cloud_controller.get_all_cloud_zones",
        return_value=[],
    ) as mock_function:
        yield mock_function


@pytest.mark.parametrize(
    "x_correlator, body, expected_response_status, expected_response_body",
    [
        (None, {}, 201, {"appId": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}),
    ],
)
def test_submit_app(
    x_correlator,
    body,
    expected_response_status,
    expected_response_body,
    mock_get_all_cloud_zones: MagicMock,
    test_app: Flask,
):
    """
    Test the get_edge_cloud_zones controller.
    """
    with test_app.test_request_context():
        response, response_status = submit_app(x_correlator, body)
        assert response_status == expected_response_status
        if expected_response_status == 400:
            assert response.json["code"] == "VALIDATION_ERROR"
        # elif expected_response_status == 201:
        #     assert len(response.json) == expected_count
        #     mock_get_all_cloud_zones.assert_called_once()
        else:
            assert False
