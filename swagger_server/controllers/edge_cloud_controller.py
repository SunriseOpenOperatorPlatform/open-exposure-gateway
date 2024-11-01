import connexion
import six

from swagger_server.models.edge_cloud_region import EdgeCloudRegion  # noqa: E501
from swagger_server.models.edge_cloud_zone_status import (
    EdgeCloudZoneStatus,
)  # noqa: E501
from swagger_server.models.edge_cloud_zones import EdgeCloudZones  # noqa: E501
from swagger_server.models.error_info import ErrorInfo  # noqa: E501
from swagger_server import util
from swagger_server.schema_mappers.edge_cloud_mapper import map_to_edge_cloud
from swagger_server.services.pi_edge_services import PiEdgeAPIClientFactory


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
        if connexion.request.is_json:
            region = EdgeCloudRegion.from_dict(
                connexion.request.get_json()
            )  # noqa: E501
        if connexion.request.is_json:
            status = EdgeCloudZoneStatus.from_dict(
                connexion.request.get_json()
            )  # noqa: E501

        pi_edge_factory = PiEdgeAPIClientFactory()
        pi_edge_api_client = pi_edge_factory.create_pi_edge_api_client()
        nodes: list | None = pi_edge_api_client.edge_cloud_zones()

        if not nodes:
            error_info = ErrorInfo(
                status=404, code="NOT_FOUND", message="No edge cloud zones found."
            )
            return error_info, 404

        # Map nodes to EdgeCloudZones
        edge_cloud_zones = [map_to_edge_cloud(zone) for zone in nodes]

        return edge_cloud_zones, 200

    except Exception as e:
        error_info = ErrorInfo(
            status=500, code="INTERNAL_ERROR", message=f"An error occurred: {str(e)}"
        )
        return error_info, 500
