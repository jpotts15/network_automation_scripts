import requests
from requests.auth import HTTPBasicAuth

def call_api(api_url, username, password):
    if username == "token":
        headers = {
            "Authorization": f"Token {password}"
        }
        response = requests.get(api_url, headers=headers)
    else:
        response = requests.get(api_url, auth=HTTPBasicAuth(username, password))
    
    return response
