from flask import jsonify
from pydantic import BaseModel, Field, ValidationError
from typing import List


class EdgeCloudZone(BaseModel):
    edgeCloudZoneId: str = Field(
        ..., description="Unique identifier of the Edge Cloud Zone"
    )
    edgeCloudZoneName: str = Field(..., description="Name of the Edge Cloud Zone")
    edgeCloudZoneStatus: str = Field(
        ...,
        description="Status of the Edge Cloud Zone",
        pattern="^(active|inactive|unknown)$",
    )
    edgeCloudProvider: str = Field(..., description="Name of the Edge Cloud Provider")
    edgeCloudRegion: str = Field(..., description="Region of the Edge Cloud Zone")


class EdgeCloudQueryParams(BaseModel):
    x_correlator: str | None
    region: str | None
    status: str | None = Field(
        ...,
        description="Status of the Edge Cloud Zone",
        pattern="^(active|inactive|unknown)$",
    )


def get_local_zones() -> List[EdgeCloudZone]:
    """get local Operator Platform available zones from Service Resource Manager"""
    return []


def get_federated_zones() -> List[EdgeCloudZone]:
    """get partner/federated Operator Platform available zones from Federation Manager"""
    return []


def get_all_cloud_zones() -> List[EdgeCloudZone]:
    """get all available zones from local and federated Operator Platforms"""
    return get_local_zones() + get_federated_zones()


def get_edge_cloud_zones(x_correlator=None, region=None, status=None):  # noqa: E501
    """Retrieve a list of the operators Edge Cloud Zones and their status

    List of the operators Edge Cloud Zones and their status, ordering the results by location and filtering by status (active/inactive/unknown)  # noqa: E501

    :param x_correlator: Correlation id for the different services
    :type x_correlator: str
    :param region: Human readable name of the geographical Edge Cloud Region of the Edge Cloud. Defined by the Edge Cloud Provider.
    :type region: dict | bytes
    :param status: Human readable status of the Edge Cloud Zone
    :type status: dict | bytes

    :rtype: EdgeCloudZones
    """
    try:
        query_params = EdgeCloudQueryParams(
            x_correlator=x_correlator,
            region=region,
            status=status,
        )

        filtered_zones = [
            zone
            for zone in get_all_cloud_zones()
            if (
                (query_params.region is None)
                or (zone["edgeCloudRegion"] == query_params.region)
            )
            and (
                (query_params.status is None)
                or (zone["edgeCloudZoneStatus"] == query_params.status)
            )
        ]
        response = [EdgeCloudZone(**zone).model_dump() for zone in filtered_zones]
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
