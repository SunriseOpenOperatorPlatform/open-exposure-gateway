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
