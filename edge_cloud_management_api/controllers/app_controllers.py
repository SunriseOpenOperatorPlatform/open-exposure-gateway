import uuid
from flask import jsonify

from pydantic import ValidationError
from edge_cloud_management_api.managers.db_manager import MongoManager
from edge_cloud_management_api.managers.log_manager import logger
from edge_cloud_management_api.models.application_models import AppManifest


class NotFound404Exception(Exception):
    pass


def submit_app(body: dict):
    """
    Controller for submitting application metadata.
    """
    try:
        # Validate the input data using Pydantic
        validated_data = AppManifest(**body)
        validated_data_dict = validated_data.model_dump(mode="json")
        validated_data_dict["_id"] = str(uuid.uuid4())
        # Insert into MongoDB
        with MongoManager() as db:
            document_id = db.insert_document("apps", validated_data_dict)
            return (
                jsonify({"appId": str(document_id)}),
                201,
            )

    except ValidationError as e:
        return jsonify({"error": "Invalid input", "details": e.errors()}), 400

    except Exception as e:
        return (
            jsonify({"error": "An unexpected error occurred", "details": str(e)}),
            500,
        )


def get_apps(x_correlator=None):  # noqa: E501
    """Retrieve metadata information of all applications"""
    try:
        with MongoManager() as db:
            documents_cursor = db.find_documents("apps", {})
            response_apps = list()
            for document in documents_cursor:
                document["appId"] = document["_id"]
                del document["_id"]
                response_apps.append(document)

            return (jsonify(response_apps), 200)

    except Exception as e:
        return (
            jsonify({"error": "An unexpected error occurred", "details": str(e)}),
            500,
        )


def get_app(appId, x_correlator=None):  # noqa: E501
    """Retrieve the information of an Application"""
    try:
        with MongoManager() as db:
            document = db.find_document("apps", {"_id": appId})
            if document is None:
                raise NotFound404Exception()
            document["appId"] = document["_id"]
            del document["_id"]

            return (jsonify(document), 200)

    except NotFound404Exception:
        return (
            jsonify({"status": 404, "code": "NOT_FOUND", "message": "Resource does not exist"}),
            404,
        )

    except Exception as e:
        return (
            jsonify({"error": "An unexpected error occurred", "details": str(e)}),
            500,
        )


def delete_app(appId, x_correlator=None):  # noqa: E501
    """Delete Application metadata from an Edge Cloud Provider"""
    try:
        with MongoManager() as db:
            number_of_deleted_documents = db.delete_document("apps", {"_id": appId})
            if number_of_deleted_documents == 0:
                raise NotFound404Exception()
            elif number_of_deleted_documents == 1:
                return ("", 204)
            else:
                raise Exception(f"deleted {number_of_deleted_documents} documents")

    except NotFound404Exception:
        return (
            jsonify({"status": 404, "code": "NOT_FOUND", "message": "Resource does not exist"}),
            404,
        )

    except Exception as e:
        return (
            jsonify({"status": 500, "code": "INTERNAL", "message": f"Internal server error: {str(e)}"}),
            500,
        )


def create_app_instance(body, app_id, x_correlator=None):  # noqa: E501
    """Instantiation of an Application

    Ask the Edge Cloud Platform to instantiate an application to one or several Edge Cloud Zones with an Application as an input and an Application Instance as the output.  # noqa: E501

    :param body: Array of Edge Cloud Zone
    :type body: list | bytes
    :param app_id: A globally unique identifier associated with the application. Edge Cloud Provider generates this identifier when the application is submitted.
    :type app_id: dict | bytes
    :param x_correlator: Correlation id for the different services
    :type x_correlator: str

    :rtype: InlineResponse202
    """
    try:
        return {}, 202  # application instantiation accepted
    except Exception:
        logger.exception("Error while creating app instance")
        error = {
            "status": 500,
            "code": "INTERNAL",
            "message": "Internal server error.",
        }
        return error, 500


def get_app_instance(app_id, x_correlator=None, app_instance_id=None, region=None):  # noqa: E501
    """Retrieve the information of Application Instances for a given App

    Ask the Edge Cloud Provider the information of the instances for a given application  # noqa: E501

    :param app_id: A globally unique identifier associated with the application. Edge Cloud Provider generates this identifier when the application is submitted.
    :type app_id: dict | bytes
    :param x_correlator: Correlation id for the different services
    :type x_correlator: str
    :param app_instance_id: A globally unique identifier associated with a running instance of an application within an specific Edge Cloud Zone. Edge Cloud Provider generates this identifier.
    :type app_instance_id: dict | bytes
    :param region: Human readable name of the geographical Edge Cloud Region of the Edge Cloud. Defined by the Edge Cloud Provider.
    :type region: dict | bytes

    :rtype: InlineResponse2001
    """
    return "do some magic!"


def delete_app_instance(app_id, app_instance_id, x_correlator=None):  # noqa: E501
    """Terminate an Application Instance

    Terminate a running instance of an application within an Edge Cloud Zone  # noqa: E501

    :param app_id: A globally unique identifier associated with the application. Edge Cloud Provider generates this identifier when the application is submitted.
    :type app_id: dict | bytes
    :param app_instance_id: Identificator of the specific application instance that will be terminated
    :type app_instance_id: dict | bytes
    :param x_correlator: Correlation id for the different services
    :type x_correlator: str

    :rtype: None
    """
    return "do some magic!"
