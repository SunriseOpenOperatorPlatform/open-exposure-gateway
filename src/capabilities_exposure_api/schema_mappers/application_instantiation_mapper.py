import re
from types import SimpleNamespace


def remove_special_characters(input_string: str):
    """
    Removes all special characters from the input string.

    Parameters:
    input_string (str): The string from which to remove special characters.

    Returns:
    str: A string with special characters removed.
    """
    # Use regex to replace any character that is not alphanumeric or a space
    cleaned_string = re.sub(r"[^a-zA-Z0-9\s]", "", input_string)
    return cleaned_string


def map_to_pi_edge_deployed_service_function(
    input: SimpleNamespace, input_service_function_name: str
):
    """
    Converts the CAMARA application instantiation input JSON schema to the desired output format for Pi Edge deployed Service Function.

    Args:
        input (SimpleNamespace): A dictionary CAMARA application instantiation information.

    Returns:
        dict: The mapped dictionary in the desired format.

    Example Input:
        {
            "edge_cloud_zone_id": "2243ab4-9886-4e5f-a4a8-f792e0d633ae",
            "edge_cloud_zone_name": "test-location",
            "edge_cloud_zone_status": "active",
            "edge_cloud_provider": "Intracom SA Telecom Solution",
            "edge_cloud_region": "GR-ATH"
        }

    Example Output:
        {
            "service_function_name": "nginx-demo",
            "service_function_instance_name": "nginxdemo",
            "location": "test-location"
        }
    """
    return {
        "service_function_name": input_service_function_name,
        "service_function_instance_name": remove_special_characters(
            f'{input_service_function_name}{input.edge_cloud_zone_name}'
        ),
        "location": input.edge_cloud_zone_name,
    }
