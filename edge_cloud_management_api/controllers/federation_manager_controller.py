from flask import request, jsonify
from edge_cloud_management_api.services.federation_services import FederationManagerClientFactory

factory = FederationManagerClientFactory()
federation_client = factory.create_federation_client()

def create_federation():
    """
    POST /partner
    Forwards the federation creation request to Federation Manager.
    """
    try:
        body = request.get_json()
        result = federation_client.post_partner(body)
        return jsonify(result), 200 if "error" not in result else 502
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def get_federation(federationContextId):
    """
    GET /{federationContextId}/partner
    Forwards the GET federation info request.
    """
    try:
        result = federation_client.get_partner(federationContextId)
        return jsonify(result), 200 if "error" not in result else 502
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def delete_federation(federationContextId):
    """
    DELETE /{federationContextId}/partner
    Forwards the DELETE federation request.
    """
    try:
        result = federation_client.delete_partner(federationContextId)
        return jsonify(result), 200 if "error" not in result else 502
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def get_federation_context_ids():
    """
    GET /fed-context-id
    Forwards the request to fetch federation context IDs.
    """
    try:
        result = federation_client.get_federation_context_ids()
        return jsonify(result), 200 if "error" not in result else 502
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def onboard_application_to_partner(federationContextId):
    """
    POST /{federationContextId}/application/onboarding
    Forwards the onboarding request to the Federation Manager.
    """
    try:
        body = request.get_json()
        result = federation_client.onboard_application(federationContextId, body)
        return jsonify(result), 202 if "error" not in result else 502
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def get_onboarded_app(federationContextId, appId):
    """
    GET /{federationContextId}/application/onboarding/app/{appId}
    Retrieves onboarding info of a federated app from a partner OP.
    """
    try:
        result = federation_client.get_onboarded_app(federationContextId, appId)
        if "error" in result:
            return jsonify(result), result.get("status_code", 502)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
def delete_onboarded_app(federationContextId, appId):
    """
    DELETE /{federationContextId}/application/onboarding/app/{appId}
    Deboards the application and deletes it from the partner OP.
    """
    try:
        result = federation_client.delete_onboarded_app(federationContextId, appId)
        if "error" in result:
            return jsonify(result), result.get("status_code", 502)
        return jsonify({"message": f"App {appId} successfully deleted from partner"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

