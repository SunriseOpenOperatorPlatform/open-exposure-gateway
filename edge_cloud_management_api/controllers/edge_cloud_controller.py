from flask import jsonify
from pydantic import BaseModel, Field, ValidationError
from typing import List
from edge_cloud_management_api.managers.log_manager import logger
from edge_cloud_management_api.services.pi_edge_services import PiEdgeAPIClientFactory



class EdgeCloudZone(BaseModel):
    edgeCloudZoneId: str = Field(..., description="Unique identifier of the Edge Cloud Zone")
    edgeCloudZoneName: str = Field(..., description="Name of the Edge Cloud Zone")
    edgeCloudZoneStatus: str = Field(
        ...,
        description="Status of the Edge Cloud Zone",
        pattern="^(active|inactive|unknown)$",
    )
    edgeCloudProvider: str = Field(..., description="Name of the Edge Cloud Provider")
    edgeCloudRegion: str | None = Field(..., description="Region of the Edge Cloud Zone")


class EdgeCloudQueryParams(BaseModel):
    x_correlator: str | None
    region: str | None
    status: str | None = Field(
        ...,
        description="Status of the Edge Cloud Zone",
        pattern="^(active|inactive|unknown)$",
    )


def get_local_zones() -> list[dict]:
    """
    Get local Operator Platform available zones from PiEdge Service Resource Manager.
    """
    try:
        pi_edge_factory = PiEdgeAPIClientFactory()
        api_client = pi_edge_factory.create_pi_edge_api_client()
        result = api_client.edge_cloud_zones()

        if isinstance(result, dict) and "error" in result:
            logger.error(f"PiEdge error: {result['error']}")
            return []

        # zones = []
        # for node in result:
        #     try:
        #         zone = EdgeCloudZone(
        #             edgeCloudZoneId=node["id"],
        #             edgeCloudZoneName=node.get("name", "unknown"),
        #             edgeCloudZoneStatus=node.get("status", "unknown"),
        #             edgeCloudProvider=node.get("provider", "local-provider"),
        #             edgeCloudRegion=node.get("region", "default-region")
        #         )
        #         zones.append(zone.model_dump())
        #     except Exception as e:
        #         logger.warning(f"Failed to parse node into EdgeCloudZone: {e}")

        return result

    except Exception as e:
        logger.exception("Unexpected error while retrieving local zones from PiEdge")
        return []


def get_federated_zones() -> List[EdgeCloudZone]:
    """get partner/federated Operator Platform available zones from Federation Manager"""
    return []


def get_all_cloud_zones() -> List[EdgeCloudZone]:
    """get all available zones from local and federated Operator Platforms"""
    return get_local_zones() + get_federated_zones()


def get_edge_cloud_zones(x_correlator: str | None = None, region=None, status=None):  # noqa: E501
    """Retrieve a list of the operators Edge Cloud Zones and their status

    List of the operators Edge Cloud Zones and their status, ordering the results by location and filtering by status (active/inactive/unknown)  # noqa: E501

    :param x_correlator: Correlation id for the different services
    :type x_correlator: str
    :param region: Human readable name of the geographical Edge Cloud Region of the Edge Cloud. Defined by the Edge Cloud Provider.
    :type region: str
    :param status: Human readable status of the Edge Cloud Zone
    :type status: str

    :rtype: list[EdgeCloudZone]
    """
    try:
        query_params = EdgeCloudQueryParams(
            x_correlator=x_correlator,
            region=region,
            status=status,
        )

        def query_region_matches(zone: str) -> bool:
            """If region is None, return True (don't apply region filtering), otherwise check if the zone region matches the query region"""
            return query_params.region is None or zone["edgeCloudRegion"] == query_params.region

        def query_status_matches(zone: str) -> bool:
            """If status is None, return True (don't apply status filtering), otherwise check if the zone status matches the query status"""
            return (query_params.status is None) or (zone["edgeCloudZoneStatus"] == query_params.status)

        # filtered_zones = [zone for zone in get_all_cloud_zones() if (query_region_matches(zone) and query_status_matches(zone))]
        
        response = [EdgeCloudZone(**zone).model_dump() for zone in get_all_cloud_zones()]
        return jsonify(response), 200

    except ValidationError as e:
        return (
            jsonify({"status": 400, "code": "VALIDATION_ERROR", "message": e.errors()}),
            400,
        )

    except Exception as e:
        error_info = {
            "status": 500,
            "code": "INTERNAL_ERROR",
            "message": f"An error occurred: {str(e)}",
        }
        return jsonify(error_info), 500
