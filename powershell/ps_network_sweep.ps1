<# Powershell Network Sweep
Takes input CSVs and scans devices for ping response, ssh or other port open and snmp walk
Created by: Joseph Potts
Version 1.0
Last Update: 31Aug2024

To Run:
.\ps_network_sweep.ps1 -pingInputPath "C:\Users\YourName\Desktop\ping.csv" -portScanInputPath "C:\Users\YourName\Desktop\portscan.csv" -snmpInputPath "C:\Users\YourName\Desktop\snmp.csv" -pingOutputPath "C:\Users\YourName\Desktop\ping_output.csv" -portScanOutputPath "C:\Users\YourName\Desktop\portscan_output.csv" -snmpOutputPath "C:\Users\YourName\Desktop\snmp_output.csv"
#>

param (
    [string]$pingInputPath,       # Path to the input CSV file for the ping sweep
    [string]$portScanInputPath,   # Path to the input CSV file for the port scan
    [string]$snmpInputPath,       # Path to the input CSV file for the SNMP sweep
    [string]$pingOutputPath,      # Path to the output CSV file for the ping sweep results
    [string]$portScanOutputPath,  # Path to the output CSV file for the port scan results
    [string]$snmpOutputPath       # Path to the output CSV file for the SNMP sweep results
)

# Function to check if a file exists
function Check-FileExists {
    param (
        [string]$filePath,
        [string]$fileDescription
    )
    if (-not (Test-Path -Path $filePath)) {
        Write-Host "$fileDescription file not found: $filePath" -ForegroundColor Red
        exit
    }
}

# Check if the input files exist
Check-FileExists -filePath $pingInputPath -fileDescription "Ping input"
Check-FileExists -filePath $portScanInputPath -fileDescription "Port scan input"
Check-FileExists -filePath $snmpInputPath -fileDescription "SNMP input"

# 1. Ping Sweep
Write-Host "Starting Ping Sweep..."
$pingResults = @()

$pingList = Import-Csv -Path $pingInputPath
foreach ($row in $pingList) {
    $ip = $row.IP
    $status = "Unreachable"
    try {
        $pingResult = Test-Connection -ComputerName $ip -Count 1 -Quiet
        if ($pingResult) {
            $status = "Reachable"
        }
    } catch {
        $status = "Unreachable"
    }
    $pingResults += [PSCustomObject]@{
        IP = $ip
        Status = $status
    }
}
$pingResults | Export-Csv -Path $pingOutputPath -NoTypeInformation
Write-Host "Ping Sweep complete. Results saved to $pingOutputPath."

# 2. Port Scanner
Write-Host "Starting Port Scan..."
$portScanResults = @()

$portList = Import-Csv -Path $portScanInputPath
foreach ($row in $portList) {
    $ip = $row.IP
    $port = $row.Port
    $status = "Closed"
    try {
        $tcpConnection = New-Object System.Net.Sockets.TcpClient($ip, $port)
        $status = "Open"
    } catch {
        $status = "Closed"
    } finally {
        if ($tcpConnection -ne $null) {
            $tcpConnection.Close()
        }
    }
    $portScanResults += [PSCustomObject]@{
        IP = $ip
        Port = $port
        Status = $status
    }
}
$portScanResults | Export-Csv -Path $portScanOutputPath -NoTypeInformation
Write-Host "Port Scan complete. Results saved to $portScanOutputPath."

# 3. SNMP Sweep
Write-Host "Starting SNMP Sweep..."
$snmpResults = @()

$snmpList = Import-Csv -Path $snmpInputPath
foreach ($row in $snmpList) {
    $ip = $row.IP
    $snmpVersion = $row.SNMPVersion
    $snmpCommand = ""

    if ($snmpVersion -eq "2") {
        $communityString = $row.CommunityString
        $snmpCommand = "snmpwalk -v2c -c $communityString $ip"
    }
    elseif ($snmpVersion -eq "3") {
        $authType = $row.AuthType
        $authPassword = $row.AuthPassword
        $privType = $row.PrivType
        $privPassword = $row.PrivPassword
        $snmpCommand = "snmpwalk -v3 -a $authType -A $authPassword -x $privType -X $privPassword $ip"
    }
    else {
        Write-Host "Unsupported SNMP version for IP $ip" -ForegroundColor Yellow
        continue
    }

    try {
        $snmpOutput = Invoke-Expression $snmpCommand
        $status = $snmpOutput ? "SNMP Walk Successful" : "SNMP Walk Failed"
        $outputData = $snmpOutput -join "`n"
    } catch {
        $status = "SNMP Walk Failed"
        $outputData = $_.Exception.Message
    }

    $snmpResults += [PSCustomObject]@{
        IP = $ip
        Status = $status
        SNMPData = $outputData
    }
}
$snmpResults | Export-Csv -Path $snmpOutputPath -NoTypeInformation
Write-Host "SNMP Sweep complete. Results saved to $snmpOutputPath."
