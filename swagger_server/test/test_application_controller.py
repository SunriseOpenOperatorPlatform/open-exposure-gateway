# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.app_id import AppId  # noqa: E501
from swagger_server.models.app_instance_id import AppInstanceId  # noqa: E501
from swagger_server.models.app_manifest import AppManifest  # noqa: E501
from swagger_server.models.edge_cloud_region import EdgeCloudRegion  # noqa: E501
from swagger_server.models.edge_cloud_zone import EdgeCloudZone  # noqa: E501
from swagger_server.models.error_info import ErrorInfo  # noqa: E501
from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.inline_response202 import InlineResponse202  # noqa: E501
from swagger_server.models.submitted_app import SubmittedApp  # noqa: E501
from swagger_server.test import BaseTestCase


class TestApplicationController(BaseTestCase):
    """ApplicationController integration test stubs"""

    def test_create_app_instance(self):
        """Test case for create_app_instance

        Instantiation of an Application
        """
        body = [EdgeCloudZone()]
        headers = [('x_correlator', 'x_correlator_example')]
        response = self.client.open(
            '/apps/{appId}/instances'.format(app_id=AppId()),
            method='POST',
            data=json.dumps(body),
            headers=headers,
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_app(self):
        """Test case for delete_app

        Delete an Application from an Edge Cloud Provider 
        """
        headers = [('x_correlator', 'x_correlator_example')]
        response = self.client.open(
            '/apps/{appId}'.format(app_id=AppId()),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_app_instance(self):
        """Test case for delete_app_instance

        Terminate an Application Instance
        """
        headers = [('x_correlator', 'x_correlator_example')]
        response = self.client.open(
            '/apps/{appId}/instances/{appInstanceId}'.format(app_id=AppId(), app_instance_id=AppInstanceId()),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_app(self):
        """Test case for get_app

        Retrieve the information of an Application
        """
        headers = [('x_correlator', 'x_correlator_example')]
        response = self.client.open(
            '/apps/{appId}'.format(app_id=AppId()),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_app_instance(self):
        """Test case for get_app_instance

        Retrieve the information of Application Instances for a given App
        """
        query_string = [('app_instance_id', AppInstanceId()),
                        ('region', EdgeCloudRegion())]
        headers = [('x_correlator', 'x_correlator_example')]
        response = self.client.open(
            '/apps/{appId}/instances'.format(app_id=AppId()),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_submit_app(self):
        """Test case for submit_app

        Submit application metadata to the Edge Cloud Provider.
        """
        body = AppManifest()
        headers = [('x_correlator', 'x_correlator_example')]
        response = self.client.open(
            '/apps',
            method='POST',
            data=json.dumps(body),
            headers=headers,
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
