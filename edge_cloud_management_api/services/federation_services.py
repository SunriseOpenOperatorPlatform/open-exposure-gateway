import requests
from requests.exceptions import Timeout, ConnectionError
from edge_cloud_management_api.configs.env_config import config
from edge_cloud_management_api.managers.log_manager import logger

class FederationManagerClient:
    def __init__(self, base_url=None):
        self.base_url = base_url or config.FEDERATION_MANAGER_HOST

    def _get_headers(self):
        return {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def post_partner(self, data: dict):
        url = f"{self.base_url}/partner"
        try:
            response = requests.post(url, json=data, headers=self._get_headers(), timeout=10)
            response.raise_for_status()
            return response.json()
        except Timeout:
            logger.error("POST /partner timed out")
            return {"error": "Request timed out"}
        except ConnectionError:
            logger.error("POST /partner connection error")
            return {"error": "Connection error"}
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"POST /partner HTTP error: {http_err}")
            return {"error": str(http_err), "status_code": response.status_code}
        except Exception as e:
            logger.error(f"POST /partner unexpected error: {e}")
            return {"error": str(e)}

    def get_partner(self, federation_context_id: str):
        url = f"{self.base_url}/{federation_context_id}/partner"
        try:
            response = requests.get(url, headers=self._get_headers(), timeout=10)
            response.raise_for_status()
            return response.json()
        except Timeout:
            logger.error("GET /{id}/partner timed out")
            return {"error": "Request timed out"}
        except ConnectionError:
            logger.error("GET /{id}/partner connection error")
            return {"error": "Connection error"}
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"GET /{id}/partner HTTP error: {http_err}")
            return {"error": str(http_err), "status_code": response.status_code}
        except Exception as e:
            logger.error(f"GET /{id}/partner unexpected error: {e}")
            return {"error": str(e)}

    def delete_partner(self, federation_context_id: str):
        url = f"{self.base_url}/{federation_context_id}/partner"
        try:
            response = requests.delete(url, headers=self._get_headers(), timeout=10)
            if response.content:
                return response.json()
            return {"status": response.status_code}
        except Timeout:
            logger.error("DELETE /{id}/partner timed out")
            return {"error": "Request timed out"}
        except ConnectionError:
            logger.error("DELETE /{id}/partner connection error")
            return {"error": "Connection error"}
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"DELETE /{id}/partner HTTP error: {http_err}")
            return {"error": str(http_err), "status_code": response.status_code}
        except Exception as e:
            logger.error(f"DELETE /{id}/partner unexpected error: {e}")
            return {"error": str(e)}

    def get_federation_context_ids(self):
        url = f"{self.base_url}/fed-context-id"
        try:
            response = requests.get(url, headers=self._get_headers(), timeout=10)
            response.raise_for_status()
            return response.json()
        except Timeout:
            logger.error("GET /fed-context-id timed out")
            return {"error": "Request timed out"}
        except ConnectionError:
            logger.error("GET /fed-context-id connection error")
            return {"error": "Connection error"}
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"GET /fed-context-id HTTP error: {http_err}")
            return {"error": str(http_err), "status_code": response.status_code}
        except Exception as e:
            logger.error(f"GET /fed-context-id unexpected error: {e}")
            return {"error": str(e)}


class FederationManagerClientFactory:
    def __init__(self):
        self.default_base_url = config.FEDERATION_MANAGER_HOST

    def create_federation_client(self, base_url=None):
        base_url = base_url or self.default_base_url
        return FederationManagerClient(base_url=base_url)


if __name__ == "__main__":
    factory = FederationManagerClientFactory()
    client = factory.create_federation_client()

    result = client.get_federation_context_ids()
    logger.info("Federation Context IDs: %s", result)
