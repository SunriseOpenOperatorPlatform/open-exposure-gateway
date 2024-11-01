def find_requested_service_function(service_functions: list, app_id: str):
    """Given a pi edge service functions catalogue, return the requested item or None

    Args:
        service_functions (list): list of service function
        app_id (str): a uuid4 id

    Returns:
        dict | None: the requested service function dict or None if not found
    """
    for item in service_functions:
        if isinstance(item, dict) and "_id" in item.keys():
            if item["_id"] == app_id:
                return item
