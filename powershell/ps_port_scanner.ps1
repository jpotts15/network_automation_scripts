<# Powershell Port Scanner
Uses powershell to check if a port is open against a list of IPs from a CSV
Created by: Joseph Potts
Version 1.0
Last Update: 31Aug2024

.\ps_port_scanner.ps1 -csvInputPath "[input csv path]" -csvOutputPath "[output csv path]"
#>

param (
    [string]$csvInputPath,   # Path to the input CSV file
    [string]$csvOutputPath,   # Path to the output CSV file
    [string]$port   # port to check
)

$port = 22  # Port to check

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
    $status = "CLOSED"  # Default status is CLOSED
    
    try {
        # Try to create a TCP connection to the specified IP and port
        $tcpConnection = New-Object System.Net.Sockets.TcpClient($ip, $port)
        $status = "OPEN"  # If connection is successful, set status to OPEN
    } catch {
        # If the connection fails, keep status as CLOSED
    } finally {
        if ($tcpConnection -ne $null) {
            $tcpConnection.Close()
        }
    }
    
    # Add the result to the array
    $results += [PSCustomObject]@{
        IP = $ip
        Status = $status
    }
}

# Export the results to a CSV file
$results | Export-Csv -Path $csvOutputPath -NoTypeInformation

Write-Host "Port check complete. Results saved to $csvOutputPath."
