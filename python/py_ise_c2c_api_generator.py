import requests
from requests.auth import HTTPBasicAuth

# Cisco ISE connection details
ISE_BASE_URL = "https://ise.lt-networks.com:9060"
ISE_USERNAME = "api_test"
ISE_PASSWORD = "api_test1234!@#$"

# Endpoint to fetch endpoint data
ENDPOINTS_API = "/ers/config/endpoint"

def get_endpoint_profiles():
    # Define headers and authentication
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    auth = HTTPBasicAuth(ISE_USERNAME, ISE_PASSWORD)

    # Fetch endpoint device report
    url = f"{ISE_BASE_URL}{ENDPOINTS_API}"
    response = requests.get(url, headers=headers, auth=auth, verify=False)

    if response.status_code != 200:
        print(f"Failed to fetch endpoints: {response.status_code}")
        return []

    # Parse the response JSON
    endpoints = response.json().get('SearchResult', {}).get('resources', [])

    # Extract endpoint profiles
    endpoint_profiles = []
    for endpoint in endpoints:
        endpoint_id = endpoint.get("id")
        
        # Fetch detailed information for each endpoint
        detail_url = f"{ISE_BASE_URL}{ENDPOINTS_API}/{endpoint_id}"
        detail_response = requests.get(detail_url, headers=headers, auth=auth, verify=False)

        if detail_response.status_code == 200:
            detail_data = detail_response.json()
            profile = detail_data.get("ERSEndPoint", {}).get("profileName")
            endpoint_profiles.append({
                "id": endpoint_id,
                "macAddress": detail_data.get("ERSEndPoint", {}).get("macAddress"),
                "profile": profile
            })
        else:
            print(f"Failed to fetch details for endpoint {endpoint_id}")

    return endpoint_profiles

# Usage
if __name__ == "__main__":
    endpoint_profiles = get_endpoint_profiles()
    for ep in endpoint_profiles:
        print(f"Endpoint ID: {ep['id']}, MAC Address: {ep['macAddress']}, Profile: {ep['profile']}")
