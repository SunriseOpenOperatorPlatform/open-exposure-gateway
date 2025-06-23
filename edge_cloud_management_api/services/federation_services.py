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

    def onboard_application(self, federation_context_id: str, body: dict):
        url = f"{self.base_url}/{federation_context_id}/application/onboarding"
        try:
           response = requests.post(url, headers=self._get_headers(), json=body, timeout=10)
           response.raise_for_status()
           return response.json()
        except: Timeout:
          logger.error("POST /application/onboarding timed out")
          return {"error": "Request timed out"}
        except: ConnectionError:
            logger.error("POST /application/onboarding connection error")
            return {"error": "Connection error"}
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"POST /application/onboarding HTTP error: {http_err}")
            return {"error": str(http_err), "status_code": response.status_code}
        except Exception as e:
            logger.error(f"POST /application/onboarding unexpected error: {e}")
            return {"error": str(e)}


    def get_onboarded_app(self, federation_context_id: str, app_id: str):
        url = f"{self.base_url}/{federation_context_id}/application/onboarding/app/{app_id}"
        try:
            response = requests.get(url, headers=self._get_headers(), timeout=10)
            response.raise_for_status()
            return response.json()
        except Timeout:
            logger.error("GET onboarded app timed out")
            return {"error": "Request timed out", "status_code": 408}
        except ConnectionError:
            logger.error("GET onboarded app connection error")
            return {"error": "Connection error", "status_code": 503}
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"GET onboarded app HTTP error: {http_err}")
            return {"error": str(http_err), "status_code": response.status_code}
        except Exception as e:
            logger.error(f"GET onboarded app unexpected error: {e}")
            return {"error": str(e), "status_code": 500}
            
    def delete_onboarded_app(self, federation_context_id: str, app_id: str):
        url = f"{self.base_url}/{federation_context_id}/application/onboarding/app/{app_id}"
        try:
            response = requests.delete(url, headers=self._get_headers(), timeout=10)
            response.raise_for_status()
            return {"message": "Deleted successfully", "status_code": response.status_code}
        except Timeout:
            logger.error("DELETE onboarding app timed out")
            return {"error": "Request timed out", "status_code": 504}
        except ConnectionError:
            logger.error("DELETE onboarding app connection error")
            return {"error": "Connection error", "status_code": 503}
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"DELETE onboarding app HTTP error: {http_err}")
            return {"error": str(http_err), "status_code": response.status_code}
        except Exception as e:
            logger.error(f"DELETE onboarding app unexpected error: {e}")
            return {"error": str(e), "status_code": 500}



class FederationManagerClientFactory:
    def __init__(self):
        self.default_base_url = config.FEDERATION_MANAGER_HOST

    def create_federation_client(self, base_url=None):
        base_url = base_url or self.default_base_url
        return FederationManagerClient(base_url=base_url)

    def onboard_application_to_partners(app_id, zones):
        SOURCE_OP = os.getenv("SOURCE_OP_ID")
        federation_context_id = os.getenv("FEDERATION_CONTEXT_ID")
        callback_url = os.getenv("STATUS_CALLBACK_URL", "http://your-callback/api/status")

        partner_zones = [zone for zone in zones if zone.get("edgeCloudProvider") != SOURCE_OP]
        if not partner_zones:
            return {"message": "No partner zones to onboard"}, 200

        srm_client = PiEdgeAPIClientFactory().create_pi_edge_api_client()
        app_data = srm_client.get_app(app_id)

        if not app_data or "error" in app_data:
            return {"error": "Failed to retrieve application metadata from SRM"}, 500

        app_manifest = app_data.get("appManifest", {})
        onboarding_payload = {
            "appId": app_id,
            "appManifest": app_manifest,
            "zones": partner_zones,
            "appStatusCallbackLink": callback_url
        }

        factory = FederationManagerClientFactory()
        federation_client = factory.create_federation_client()

        results = []
        for zone in partner_zones:
            partner_op = zone["edgeCloudProvider"]
            try:
                response = federation_client.onboard_application(federation_context_id, onboarding_payload)
                results.append({
                    "zoneId": zone.get("edgeCloudZoneId"),
                    "provider": partner_op,
                    "status": response.get("status", "success"),
                    "detail": response
                })
            except Exception as e:
                results.append({
                    "zoneId": zone.get("edgeCloudZoneId"),
                    "provider": partner_op,
                    "status": "error",
                    "detail": str(e)
                })

        return {"onboardingResults": results}, 202
  

if __name__ == "__main__":
    factory = FederationManagerClientFactory()
    client = factory.create_federation_client()

    result = client.get_federation_context_ids()
    logger.info("Federation Context IDs: %s", result)
