# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.edge_cloud_region import EdgeCloudRegion  # noqa: E501
from swagger_server.models.edge_cloud_zone_status import EdgeCloudZoneStatus  # noqa: E501
from swagger_server.models.edge_cloud_zones import EdgeCloudZones  # noqa: E501
from swagger_server.models.error_info import ErrorInfo  # noqa: E501
from swagger_server.test import BaseTestCase


class TestEdgeCloudController(BaseTestCase):
    """EdgeCloudController integration test stubs"""

    def test_get_edge_cloud_zones(self):
        """Test case for get_edge_cloud_zones

        Retrieve a list of the operators Edge Cloud Zones and their status
        """
        query_string = [('region', EdgeCloudRegion()),
                        ('status', EdgeCloudZoneStatus())]
        headers = [('x_correlator', 'x_correlator_example')]
        response = self.client.open(
            '/edge-cloud-zones',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
