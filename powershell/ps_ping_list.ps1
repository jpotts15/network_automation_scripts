<# Powershell Ping List
Pings a list of IPs from a CSV and outputs to a csv
Created by: Joseph Potts
Version 1.0
Last Update: 31Aug2024

To Run:
.\ps_ping_list.ps1 -csvInputPath "[input csv path]" -csvOutputPath "[output csv path]"
#>


param (
    [string]$csvInputPath,   # Path to the input CSV file
    [string]$csvOutputPath   # Path to the output CSV file
)

# Check if the input file exists
if (-not (Test-Path -Path $csvInputPath)) {
    Write-Host "Input file not found: $csvInputPath" -ForegroundColor Red
    exit
}

# Import the CSV file
$ipList = Import-Csv -Path $csvInputPath

# Initialize an array to store the results
$results = @()

# Loop through each IP address in the CSV file
foreach ($row in $ipList) {
    $ip = $row.IP  # Assuming the CSV has a column named 'IP'
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

