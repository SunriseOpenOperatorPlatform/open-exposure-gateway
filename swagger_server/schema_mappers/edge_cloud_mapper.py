def map_to_edge_cloud(input: dict):
    """
    Converts the input JSON schema to the desired output format for Edge Cloud Zone.

    Args:
        input (dict): A dictionary containing edge cloud zone information.

    Returns:
        dict: The mapped dictionary in the desired format.

    Example Input:
        {
            "_id": "2243ab4-9886-4e5f-a4a8-f792e0d633ae",
            "location": "test-location",
            "name": "eerpcext-k8s",
            "node_type": "server",
            "serial": "128.3.43.5"
        }

    Example Output:
        {
            "edgeCloudZoneId": "2243ab4-9886-4e5f-a4a8-f792e0d633ae",
            "edgeCloudZoneName": "test-location",
            "edgeCloudZoneStatus": "active",
            "edgeCloudProvider": "Intracom SA Telecom Solution",
            "edgeCloudRegion": "GR-ATH"
        }
    """
    return {
        "edgeCloudZoneId": input.get("_id"),
        "edgeCloudZoneName": input.get("location"),
        "edgeCloudZoneStatus": "active",
        "edgeCloudProvider": "",
        "edgeCloudRegion": "",
    }
