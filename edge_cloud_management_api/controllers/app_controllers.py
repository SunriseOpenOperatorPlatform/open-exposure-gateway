from flask import jsonify

from pydantic import ValidationError

# from edge_cloud_management_api.models.application_models import AppManifest


def submit_app(body: dict):
    """
    Controller for submitting application metadata.
    """
    try:
        # Validate the input data using Pydantic
        # validated_data = AppManifest(**body)

        # Insert into MongoDB
        # app_id = mongo.db.applications.insert_one(validated_data.dict()).inserted_id
        app_id = 3
        return (
            jsonify(
                {"message": "Application submitted successfully!", "appId": str(app_id)}
            ),
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
    """Retrieve the information of an Application

    Ask the Edge Cloud Provider the information for a given application  # noqa: E501

    :param app_id: A globally unique identifier associated with the application. Edge Cloud Provider generates this identifier when the application is submitted.
    :type app_id: dict | bytes
    :param x_correlator: Correlation id for the different services
    :type x_correlator: str

    :rtype: InlineResponse200
    """
    # if connexion.request.is_json:
    #     app_id = AppId.from_dict(connexion.request.get_json())  # noqa: E501
    return "do some magic!"


def get_app(appId, x_correlator=None):  # noqa: E501
    """Retrieve the information of an Application

    Ask the Edge Cloud Provider the information for a given application  # noqa: E501

    :param appId: A globally unique identifier associated with the application. Edge Cloud Provider generates this identifier when the application is submitted.
    :type appId: dict | bytes
    :param x_correlator: Correlation id for the different services
    :type x_correlator: str

    :rtype: InlineResponse200
    """
    # if connexion.request.is_json:
    #     app_id = AppId.from_dict(connexion.request.get_json())  # noqa: E501
    return "do some magic!"


def delete_app(appId, x_correlator=None):  # noqa: E501
    """Delete an Application from an Edge Cloud Provider

    Delete all the information and content related to an Application # noqa: E501

    :param appId: Identificator of the application to be deleted provided by the Edge Cloud Provider once the submission was successful
    :type appId: dict | bytes
    :param x_correlator: Correlation id for the different services
    :type x_correlator: str

    :rtype: None
    """
    return "do some magic!"


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
    except:
        error = {
            "status": 500,
            "code": "INTERNAL",
            "message": "Internal server error.",
        }
        return error, 500


def get_app_instance(
    app_id, x_correlator=None, app_instance_id=None, region=None
):  # noqa: E501
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
