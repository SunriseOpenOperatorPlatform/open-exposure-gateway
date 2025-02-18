import pytest
from unittest.mock import MagicMock, patch
from flask import Flask
from edge_cloud_management_api.app import get_app_instance
from edge_cloud_management_api.controllers.app_controllers import submit_app, get_apps, get_app


@pytest.fixture
def test_app():
    """Get the Flask app instance.
    This fixture allows us to test the controllers,
    including the request context as it would be in a real HTTP request.
    """
    flask_app = get_app_instance()
    return flask_app.app


@pytest.fixture
def mock_get_all_cloud_zones():
    with patch(
        "edge_cloud_management_api.controllers.edge_cloud_controller.get_all_cloud_zones",
        return_value=[],
    ) as mock_function:
        yield mock_function


example_submit_input = {
    "name": "etO2zndyzpL1P",
    "appProvider": "TBPhbx4MO6n",
    "version": "string",
    "packageType": "QCOW2",
    "operatingSystem": {"architecture": "x86_64", "family": "RHEL", "version": "OS_VERSION_UBUNTU_2204_LTS", "license": "OS_LICENSE_TYPE_FREE"},
    "appRepo": {
        "type": "PRIVATEREPO",
        "imagePath": "https://charts.bitnami.com/bitnami/helm/example-chart:0.1.0",
        "userName": "string",
        "credentials": "string",
        "authType": "DOCKER",
        "checksum": "string",
    },
    "requiredResources": {},
    "componentSpec": [{"componentName": "string", "networkInterfaces": [{"interfaceId": "zKJ9YWHujxe73gorEzEImKfr6", "protocol": "TCP", "port": 65535, "visibilityType": "VISIBILITY_EXTERNAL"}]}],
}


@pytest.mark.parametrize(
    "x_correlator, body, expected_response_status, expected_response_body",
    [(None, example_submit_input, 201, {"appId": "3fa85f64-5717-4562-b3fc-2c963f66afa6"})],
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
    Test the submit_app controller.
    """
    with test_app.test_request_context():
        response, response_status = submit_app(body)
        assert response_status == expected_response_status
        if expected_response_status == 400:
            assert response.json["code"] == "VALIDATION_ERROR"
        elif expected_response_status == 201:
            assert "appId" in response.json
            # assert len(response.json) == expected_count
            # mock_get_all_cloud_zones.assert_called_once()
        else:
            assert False


@pytest.mark.parametrize(
    "x_correlator, expected_response_status",
    [(None, 200)],
)
def test_get_apps(
    x_correlator,
    expected_response_status,
    test_app: Flask,
):
    """
    Test the get_apps controller.
    """
    with test_app.test_request_context():
        response, response_status = get_apps(x_correlator)
        assert response_status == expected_response_status
        # if expected_response_status == 200:
        #     assert "appId" in response.json
        # else:
        #     assert False


@pytest.mark.parametrize(
    "x_correlator, app_id, expected_response_status",
    [
        (None, "e343569e-e92c-4adc-9719-468b3b00a9d3", 200),
        (None, "e343569e-192c-4adc-9719-468b3b00a9d3", 404),
    ],
)
def test_get_app(
    x_correlator,
    app_id,
    expected_response_status,
    test_app: Flask,
):
    """
    Test the get_app controller.
    """
    with test_app.test_request_context():
        response, response_status = get_app(appId=app_id, x_correlator=x_correlator)
        assert response_status == expected_response_status
