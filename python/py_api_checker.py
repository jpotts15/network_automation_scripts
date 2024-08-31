"""
Python function to check an api

Created by: Joseph Potts
Version 1.0
Last Update: 31Aug2024

# Example usage:
api_url = "https://api.example.com/data"
username = "your_username"
password = "your_password"  # or API token if username is "token"

response = call_api(api_url, username, password)

# Check the status and content of the response
if response.ok:
    print("Response Data:", response.json())
else:
    print("Error:", response.status_code, response.text)
"""

import requests
from requests.auth import HTTPBasicAuth

def call_api(api_url, username, password):
    """
    Calls the API with the given URL, username, and password.

    Args:
        api_url (str): The URL of the API endpoint.
        username (str): The username for authentication.
        password (str): The password or token for authentication.

    Returns:
        response: The HTTP response object from the API call.
    """
    # Determine if we're using token-based or basic authentication
    if username == "token":
        headers = {
            "Authorization": f"Token {password}"
        }
        response = requests.get(api_url, headers=headers)
    else:
        response = requests.get(api_url, auth=HTTPBasicAuth(username, password))
    
    return response