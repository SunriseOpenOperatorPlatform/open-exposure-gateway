import json
import pathlib
import pymongo
import pytest
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


@pytest.fixture(scope="function")
def mongo_load_apps_collection_data():
    """Fixture to insert specific test data into a MongoDB collection before running app controllers tests."""
    from edge_cloud_management_api.configs.env_config import config

    if not config.MONGO_URI:
        raise ValueError("MONGO_URI is not set in the environment configuration.")

    # rely on the loaded environmental variables to maintain consistency across app and tests
    client = pymongo.MongoClient(config.MONGO_URI)
    db_name: str = config.MONGO_URI.split("/")[-1].split("?")[0]
    db = client[db_name]

    tests_fixtures_base_path = pathlib.Path(__file__).resolve().parent.parent.parent
    with open(tests_fixtures_base_path / "fixtures/mongo-apps-test-collection-dump.json") as f:
        data = json.load(f)

    collection = db["apps"]
    if db_name != "test_db":
        raise ValueError(
            "Tests do disrupt the database collection data. To make sure it doesn't delete any production data by mistake, the test database must have a name of 'test_db'. If by error you try to execute tests against your production db, this check should protect you."
        )
    collection.delete_many({})
    collection.insert_many(data)

    client.close()


@pytest.fixture
def success_submit_pair():
    tests_path = pathlib.Path(__file__).resolve().parent.parent.parent
    with open(tests_path / "fixtures/submit-app-sample.json") as f:
        data = json.load(f)
    return data, 201


@pytest.mark.component
def test_submit_app(
    success_submit_pair,
    test_app: Flask,
):
    """
    Test the submit_app controller.
    """
    request_body, expected_response_status = success_submit_pair
    with test_app.test_request_context():
        response, response_status = submit_app(request_body)
        assert response_status == expected_response_status
        if expected_response_status == 400:
            assert response.json["code"] == "VALIDATION_ERROR"
        elif expected_response_status == 201:
            assert "appId" in response.json
        else:
            assert False


@pytest.mark.component
@pytest.mark.parametrize(
    "x_correlator, expected_response_status",
    [(None, 200)],
)
def test_get_apps(
    x_correlator,
    expected_response_status,
    mongo_load_apps_collection_data,
    test_app: Flask,
):
    """
    Test the get_apps controller.
    """
    with test_app.test_request_context():
        response, response_status = get_apps(x_correlator)
        assert response_status == expected_response_status


@pytest.mark.component
@pytest.mark.parametrize(
    "x_correlator, app_id, expected_response_status",
    [
        (None, "17b1b16b-5202-4ab6-9262-de53537ed787", 200),
        (None, "e343569e-192c-4adc-9719-468b3b00a9d3", 404),
    ],
)
def test_get_app(
    x_correlator,
    app_id,
    expected_response_status,
    mongo_load_apps_collection_data,
    test_app: Flask,
):
    """
    Test the get_app controller.
    """
    with test_app.test_request_context():
        response, response_status = get_app(appId=app_id, x_correlator=x_correlator)
        assert response_status == expected_response_status
