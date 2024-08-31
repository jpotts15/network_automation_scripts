<# Powershell Ping Sweep
Pings a range of IPs
Created by: Joseph Potts
Version 1.0
Last Update: 31Aug2024

To Run:
.\ps_ping_sweep.ps1 -startIP "192.168.1.1" -endIP "192.168.1.254" -csvOutputPath "[csv output path]"
#>
param (
    [string]$startIP,        # Start IP address
    [string]$endIP,          # End IP address
    [string]$csvOutputPath   # Path to the output CSV file
)

# Function to convert an IP address to an integer
function Convert-IpToInt {
    param (
        [string]$ipAddress
    )
    $ipBytes = [System.Net.IPAddress]::Parse($ipAddress).GetAddressBytes()
    [Array]::Reverse($ipBytes)
    return [BitConverter]::ToUInt32($ipBytes, 0)
}

# Function to convert an integer back to an IP address
function Convert-IntToIp {
    param (
        [int]$ipInt
    )
    $ipBytes = [BitConverter]::GetBytes($ipInt)
    [Array]::Reverse($ipBytes)
    return [System.Net.IPAddress]::new($ipBytes).ToString()
}

# Convert start and end IP addresses to integers
$startIPInt = Convert-IpToInt -ipAddress $startIP
$endIPInt = Convert-IpToInt -ipAddress $endIP

# Initialize an array to store the results
$results = @()

# Loop through each IP address in the range
for ($ipInt = $startIPInt; $ipInt -le $endIPInt; $ipInt++) {
    $ip = Convert-IntToIp -ipInt $ipInt
    $status = "Unreachable"  # Default status is Unreachable
    
    try {
        # Send a ping request to the IP address
        $pingResult = Test-Connection -ComputerName $ip -Count 1 -Quiet
        if ($pingResult) {
            $status = "Reachable"  # If the ping is successful, set status to Reachable
        }
    } catch {
        # If the ping fails, keep status as Unreachable
    }
    
    # Add the result to the array
    $results += [PSCustomObject]@{
        IP = $ip
        Status = $status
    }
}

# Export the results to a CSV file
$results | Export-Csv -Path $csvOutputPath -NoTypeInformation

Write-Host "Ping sweep complete. Results saved to $csvOutputPath."
