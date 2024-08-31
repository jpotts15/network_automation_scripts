<# Powershell Cisco Command Runner
Uses PS to ssh to cisco devices and run show commands
Created by: Joseph Potts
Version 1.0
Last Update: 31Aug2024

To Run:
.\ps_cisco_command_runner.ps1 -Username [username] -Command [show commands] -CSVInputPath [csv input file] -CSVOutputFile [csv output file]
#>

# Function to prompt for the password
function Get-Password {
    [System.Security.SecureString]$securePassword = Read-Host -AsSecureString "Enter Password"
    return $securePassword
}

# Parameters for the script
param (
    [Parameter(Mandatory = $true)]
    [string]$Username,

    [Parameter(Mandatory = $true)]
    [string]$Command,

    [Parameter(Mandatory = $true)]
    [string]$CSVInputPath,

    [Parameter(Mandatory = $true)]
    [string]$CSVOutputFile
)

# Import the device IPs from the CSV file
try {
    $devices = Import-Csv -Path $CSVInputPath
} catch {
    Write-Error "Failed to import CSV file. Ensure the file exists and is properly formatted."
    exit
}

# Prompt for the password
$password = Get-Password

# Initialize an array to store the results
$results = @()

# Iterate through each device and run the specified command
foreach ($device in $devices) {
    $ip = $device.IP
    Write-Host "Connecting to $ip..." -ForegroundColor Yellow

    try {
        # Create a new SSH session using New-PSSession
        $session = New-PSSession -HostName $ip -UserName $Username -SSHTransport -Password $password

        if ($session) {
            Write-Host "Connected to $ip. Running command..." -ForegroundColor Green

            # Run the command using Invoke-Command
            $output = Invoke-Command -Session $session -ScriptBlock { param($cmd) $cmd } -ArgumentList $Command

            # Store the result in the results array
            $results += [pscustomobject]@{
                IPAddress = $ip
                CommandOutput = $output -join "`n"
            }

            # Close the session
            Remove-PSSession -Session $session
        }
    } catch {
        Write-Error "Failed to connect to $ip or run the command. Error: $_"
        # Store the error in the results array
        $results += [pscustomobject]@{
            IPAddress = $ip
            CommandOutput = "Error: $_"
        }
    }
}

# Export the results to the specified CSV file
try {
    $results | Export-Csv -Path $CSVOutputFile -NoTypeInformation -Force
    Write-Host "Results have been written to $CSVOutputFile" -ForegroundColor Green
} catch {
    Write-Error "Failed to write results to CSV file. Error: $_"
}
