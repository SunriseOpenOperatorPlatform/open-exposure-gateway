import uuid
from flask import jsonify, request
from pydantic import ValidationError
from edge_cloud_management_api.managers.db_manager import MongoManager
from edge_cloud_management_api.managers.log_manager import logger
from edge_cloud_management_api.models.application_models import AppManifest, AppZones, AppInstance
from edge_cloud_management_api.services.pi_edge_services import PiEdgeAPIClientFactory
from edge_cloud_management_api.services.pi_edge_services import PiEdgeAPIClient


class NotFound404Exception(Exception):
    pass


def submit_app(body: dict):
    """
    Controller for submitting application metadata.
    """
    try:
        # Validate the input data using Pydantic
        # validated_data = AppManifest(**body)
        # validated_data_dict = validated_data.model_dump(mode="json")
        # validated_data_dict["_id"] = str(uuid.uuid4())
        pi_edge_factory = PiEdgeAPIClientFactory()
        api_client = pi_edge_factory.create_pi_edge_api_client()
        response = api_client.submit_app(body)
        # Insert into MongoDB
        # with MongoManager() as db:
        #     document_id = db.insert_document("apps", validated_data_dict)
        #     return (
        #         jsonify({"appId": str(document_id)}),
        #         201,
        #     )
        return response

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
        pi_edge_factory = PiEdgeAPIClientFactory()
        api_client = pi_edge_factory.create_pi_edge_api_client()
        registered_apps = api_client.get_service_functions_catalogue()
        return registered_apps
        # with MongoManager() as db:
        #     documents_cursor = db.find_documents("apps", {})
        #     response_apps = list()
        #     for document in documents_cursor:
        #         document["appId"] = document["_id"]
        #         del document["_id"]
        #         response_apps.append(document)

        #     return (jsonify(response_apps), 200)
    except Exception as e:
        return (
            jsonify({"error": "An unexpected error occurred", "details": str(e)}),
            500,
        )


def get_app(appId, x_correlator=None):  # noqa: E501
    """Retrieve the information of an Application"""
    try:
        pi_edge_factory = PiEdgeAPIClientFactory()
        api_client = pi_edge_factory.create_pi_edge_api_client()
        response = api_client.get_app(appId)
        return response
        # with MongoManager() as db:
        #     document = db.find_document("apps", {"_id": appId})
        #     if document is None:
        #         raise NotFound404Exception()
        #     document["appId"] = document["_id"]
        #     del document["_id"]

        #     return (jsonify(document), 200)

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
        pi_edge_factory = PiEdgeAPIClientFactory()
        api_client = pi_edge_factory.create_pi_edge_api_client()
        response = api_client.delete_app(appId=appId)
        return response.json()
        # with MongoManager() as db:
        #     number_of_deleted_documents = db.delete_document("apps", {"_id": appId})
        #     if number_of_deleted_documents == 0:
        #         raise NotFound404Exception()
        #     elif number_of_deleted_documents == 1:
        #         return ("", 204)
        #     else:
        #         raise Exception(f"deleted {number_of_deleted_documents} documents")

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


def create_app_instance():
    logger.info("Received request to create app instance")
    
    try: 
        
       body = request.get_json()
       logger.debug(f"Request body: {body}")
       
       app_id = body.get("appId")
       edge_zone_id = body.get("edgeCloudZoneId")
       k8s_ref = body.get("kubernetesClusterRef")
       
       if not app_id or not edge_zone_id or not k8s_ref:
           return jsonify({"error": "Missing required fields: appId, edgeCloudZoneId, or kubernetesCLusterRef"}), 400
       
       logger.info(f"Preparing to send deployment request to SRM for appId={app_id}")
       
       pi_edge_client_factory = PiEdgeAPICLientFactory()
       pi_edge_client = pi_edge_client_factory.create_pi_edge_api_client()
       
       print("\n === Preparing Deployment Request ===")
       print(f" Endpoint: {pi_edge_client.base_url}/deployedServiceFunction")
       print(f" Headers: {pi_edge_client._get_headers()}")
       print(f"Payload: {body}")
       print("=== End of Deployment Request ===\n")
       
       try:
          response = pi_edge_client_deploy_service_function(data=body)
          
          if isinstance(response, dict) and "error" in response:
              logger.warning(f"Failed to deploy service function: {response}")
              return jsonify({
                  "warning": "Deployment not completed (SRM service unreachable)",
                  "details": response
                  
              }), 202
              
          logger.info(f"Deployment response from SRM: {response}")
       except Exception as inner_error:
           logger.error(f"Exception while trying to deploy to SRM: {inner_error}")
           return jsonify({
               "warning": "SRM backend unavailable. Deployment request was built correctly.",
               "details": str(inner_error)
           }),202
           
       return jsonify({"message": f"Application {app_id} instantiation accepted"}), 202
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify({"error": "Validation error", "details": str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error in create_app_instance:{str(e)}")
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500   

def get_app_instance(app_id=None, x_correlator=None, app_instance_id=None, region=None):
    """
    Retrieve application instances from the database.
    Supports filtering by app_id, app_instance_id, and region.
    """
    try:
        # query = {}
        # if app_id:
        #     query["appId"] = app_id
        # if app_instance_id:
        #     query["appInstanceId"] = app_instance_id
        # if region:
        #     query["edgeCloudZone.edgeCloudRegion"] = region

        # with MongoManager() as db:
        #     instances = list(db.find_documents("appinstances", query))
        instances = None
        pi_edge_client_factory = PiEdgeAPIClientFactory()
        pi_edge_client = pi_edge_client_factory.create_pi_edge_api_client()

        if app_id is None and app_instance_id is None:
            instances = pi_edge_client.get_app_instances()

        if not instances:
            return jsonify({
                "status": 404,
                "code": "NOT_FOUND",
                "message": "No application instances found for the given parameters."
            }), 404

        return jsonify({"appInstanceInfo": instances}), 200

    except Exception as e:
        logger.exception("Failed to retrieve app instances")
        return jsonify({
            "status": 500,
            "code": "INTERNAL",
            "message": f"Internal server error: {str(e)}"
        }), 500


def delete_app_instance(appInstanceId: str, x_correlator=None):
    """
    Terminate an Application Instance

    - Removes a specific app instance from the database.
    - Returns 204 if deleted, 404 if not found.
    """
    try:
        pi_edge_client_factory = PiEdgeAPIClientFactory()
        pi_edge_client = pi_edge_client_factory.create_pi_edge_api_client()
        response = pi_edge_client.delete_app_instance(appInstanceId)
        return jsonify({'result': response.text, 'status': response.status_code})
        # with MongoManager() as db:
        #     query = {
        #         "appInstanceId": app_instance_id,
        #         "appId": app_id
        #     }
        #     deleted_count = db.delete_document("appinstances", query)

        #     if deleted_count == 0:
        #         return (
        #             jsonify({
        #                 "status": 404,
        #                 "code": "NOT_FOUND",
        #                 "message": "App instance not found"
        #             }),
        #             404,
        #         )

        #     return "", 204  # Successfully deleted

    except Exception as e:
        return (
            jsonify({
                "status": 500,
                "code": "INTERNAL",
                "message": f"Internal server error: {str(e)}"
            }),
            500,
        )
