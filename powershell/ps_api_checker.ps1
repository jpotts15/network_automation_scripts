<# Powershell API Checker
Uses PS to check a API
Created by: Joseph Potts
Version 1.0
Last Update: 31Aug2024

To Run with username/pass:
.\ps_api_checker.api -ApiUrl $ApiUrl -Username [api username] -Password [api password]
To Run with API token:
.\ps_api_checker.api -ApiUrl $ApiUrl -Username "token" -Password [api_token]
#>

# Define the function to check the device API
function Check-DeviceAPI {
    param (
        [string]$ApiUrl,
        [string]$Username,
        [string]$Password
    )

    # Determine if the authentication method is using a token
    if ($Username -eq "token") {
        # Use the token for Bearer authentication
        $Headers = @{
            Authorization = "Bearer $Password"
        }
    } else {
        # Use Basic Authentication with username and password
        $EncodedAuth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("$Username:$Password"))
        $Headers = @{
            Authorization = "Basic $EncodedAuth"
        }
    }

    try {
        # Send a GET request to the API URL
        $Response = Invoke-RestMethod -Uri $ApiUrl -Headers $Headers -Method Get
        Write-Output "API request successful. Response:"
        Write-Output $Response
    } catch {
        Write-Output "Failed to connect to the API. Error details:"
        Write-Output $_.Exception.Message
    }
}
