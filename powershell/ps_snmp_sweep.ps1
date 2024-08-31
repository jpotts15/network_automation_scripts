<# Powershell SNMP List Walk
SNMP Walk against a list of IPs from a CSV
Created by: Joseph Potts
Version 1.0
Last Update: 31Aug2024

.\ps_snmp_sweep.ps1 -csvInputPath "[csv input path]" -csvOutputPath "[csv output path]"

Input File Formats:
SNMPv2 Example Input CSV:
IP,SNMPVersion,CommunityString
192.168.1.1,2,public
192.168.1.2,2,private

SNMPv3 Example Input CSV:
IP,SNMPVersion,AuthType,AuthPassword,PrivType,PrivPassword
192.168.1.3,3,SHA,myAuthPassword,AES,myPrivPassword
192.168.1.4,3,MD5,myAuthPassword,DES,myPrivPassword
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

# Loop through each entry in the CSV file
foreach ($row in $ipList) {
    $ip = $row.IP
    $snmpVersion = $row.SNMPVersion

    # Initialize the SNMP command based on the SNMP version
    $snmpCommand = ""

    if ($snmpVersion -eq "2") {
        $communityString = $row.CommunityString
        # SNMPv2 command
        $snmpCommand = "snmpwalk -v2c -c $communityString $ip"
    }
    elseif ($snmpVersion -eq "3") {
        $authType = $row.AuthType
        $authPassword = $row.AuthPassword
        $privType = $row.PrivType
        $privPassword = $row.PrivPassword
        # SNMPv3 command
        $snmpCommand = "snmpwalk -v3 -a $authType -A $authPassword -x $privType -X $privPassword $ip"
    }
    else {
        Write-Host "Unsupported SNMP version for IP $ip" -ForegroundColor Yellow
        continue
    }

    try {
        # Execute the SNMP walk command
        $snmpOutput = Invoke-Expression $snmpCommand

        # Check if the SNMP walk was successful
        if ($snmpOutput) {
            $status = "SNMP Walk Successful"
            $outputData = $snmpOutput -join "`n"  # Join the output lines into a single string
        } else {
            $status = "SNMP Walk Failed"
            $outputData = "No data returned"
        }
    } catch {
        $status = "SNMP Walk Failed"
        $outputData = $_.Exception.Message
    }
    
    # Add the result to the array
    $results += [PSCustomObject]@{
        IP = $ip
        Status = $status
        SNMPData = $outputData
    }
}

# Export the results to a CSV file
$results | Export-Csv -Path $csvOutputPath -NoTypeInformation

Write-Host "SNMP walk complete. Results saved to $csvOutputPath."
