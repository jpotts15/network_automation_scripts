<# Powershell Cisco Command Runner GUI
Uses PS to ssh to cisco devices and run show commands with a GUI
Created by: Joseph Potts
Version 1.0
Last Update: 31Aug2024

To Run:
.\ps_cisco_command_runner_gui.ps1
#>

# Load necessary assemblies
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Function to prompt for the password
function Get-Password {
    $passwordForm = New-Object System.Windows.Forms.Form
    $passwordForm.Text = "Enter Password"
    $passwordForm.Size = New-Object System.Drawing.Size(300,150)
    $passwordForm.StartPosition = "CenterScreen"

    $label = New-Object System.Windows.Forms.Label
    $label.Text = "Password:"
    $label.Location = New-Object System.Drawing.Point(10,20)
    $passwordForm.Controls.Add($label)

    $passwordBox = New-Object System.Windows.Forms.TextBox
    $passwordBox.UseSystemPasswordChar = $true
    $passwordBox.Location = New-Object System.Drawing.Point(10,40)
    $passwordBox.Size = New-Object System.Drawing.Size(260,20)
    $passwordForm.Controls.Add($passwordBox)

    $okButton = New-Object System.Windows.Forms.Button
    $okButton.Text = "OK"
    $okButton.Location = New-Object System.Drawing.Point(200,70)
    $okButton.Add_Click({ $passwordForm.Close() })
    $passwordForm.Controls.Add($okButton)

    $passwordForm.ShowDialog()
    return $passwordBox.Text
}

# Create the form
$form = New-Object System.Windows.Forms.Form
$form.Text = "Cisco Command Runner"
$form.Size = New-Object System.Drawing.Size(400,250)
$form.StartPosition = "CenterScreen"

# Username label and textbox
$usernameLabel = New-Object System.Windows.Forms.Label
$usernameLabel.Text = "Username:"
$usernameLabel.Location = New-Object System.Drawing.Point(10,20)
$form.Controls.Add($usernameLabel)

$usernameBox = New-Object System.Windows.Forms.TextBox
$usernameBox.Location = New-Object System.Drawing.Point(120,20)
$usernameBox.Size = New-Object System.Drawing.Size(250,20)
$form.Controls.Add($usernameBox)

# Command label and textbox
$commandLabel = New-Object System.Windows.Forms.Label
$commandLabel.Text = "Command:"
$commandLabel.Location = New-Object System.Drawing.Point(10,60)
$form.Controls.Add($commandLabel)

$commandBox = New-Object System.Windows.Forms.TextBox
$commandBox.Location = New-Object System.Drawing.Point(120,60)
$commandBox.Size = New-Object System.Drawing.Size(250,20)
$form.Controls.Add($commandBox)

# Input CSV file label and textbox
$csvInputLabel = New-Object System.Windows.Forms.Label
$csvInputLabel.Text = "Input CSV File:"
$csvInputLabel.Location = New-Object System.Drawing.Point(10,100)
$form.Controls.Add($csvInputLabel)

$csvInputBox = New-Object System.Windows.Forms.TextBox
$csvInputBox.Location = New-Object System.Drawing.Point(120,100)
$csvInputBox.Size = New-Object System.Drawing.Size(180,20)
$form.Controls.Add($csvInputBox)

$browseInputButton = New-Object System.Windows.Forms.Button
$browseInputButton.Text = "Browse..."
$browseInputButton.Location = New-Object System.Drawing.Point(310,100)
$browseInputButton.Add_Click({
    $openFileDialog = New-Object System.Windows.Forms.OpenFileDialog
    $openFileDialog.Filter = "CSV Files (*.csv)|*.csv|All Files (*.*)|*.*"
    if ($openFileDialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
        $csvInputBox.Text = $openFileDialog.FileName
    }
})
$form.Controls.Add($browseInputButton)

# Output CSV file label and textbox
$csvOutputLabel = New-Object System.Windows.Forms.Label
$csvOutputLabel.Text = "Output CSV File:"
$csvOutputLabel.Location = New-Object System.Drawing.Point(10,140)
$form.Controls.Add($csvOutputLabel)

$csvOutputBox = New-Object System.Windows.Forms.TextBox
$csvOutputBox.Location = New-Object System.Drawing.Point(120,140)
$csvOutputBox.Size = New-Object System.Drawing.Size(180,20)
$form.Controls.Add($csvOutputBox)

$browseOutputButton = New-Object System.Windows.Forms.Button
$browseOutputButton.Text = "Browse..."
$browseOutputButton.Location = New-Object System.Drawing.Point(310,140)
$browseOutputButton.Add_Click({
    $saveFileDialog = New-Object System.Windows.Forms.SaveFileDialog
    $saveFileDialog.Filter = "CSV Files (*.csv)|*.csv|All Files (*.*)|*.*"
    if ($saveFileDialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
        $csvOutputBox.Text = $saveFileDialog.FileName
    }
})
$form.Controls.Add($browseOutputButton)

# Run button
$runButton = New-Object System.Windows.Forms.Button
$runButton.Text = "Run"
$runButton.Location = New-Object System.Drawing.Point(300,180)
$runButton.Add_Click({
    $username = $usernameBox.Text
    $command = $commandBox.Text
    $csvInputPath = $csvInputBox.Text
    $csvOutputFile = $csvOutputBox.Text

    if (-not $username -or -not $command -or -not $csvInputPath -or -not $csvOutputFile) {
        [System.Windows.Forms.MessageBox]::Show("Please fill in all fields.", "Validation Error", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Warning)
        return
    }

    # Prompt for the password
    $password = Get-Password
    $securePassword = ConvertTo-SecureString $password -AsPlainText -Force

    # Import the device IPs from the CSV file
    try {
        $devices = Import-Csv -Path $csvInputPath
    } catch {
        [System.Windows.Forms.MessageBox]::Show("Failed to import CSV file. Ensure the file exists and is properly formatted.", "Error", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error)
        return
    }

    # Initialize an array to store the results
    $results = @()

    # Iterate through each device and run the specified command
    foreach ($device in $devices) {
        $ip = $device.IP
        Write-Host "Connecting to $ip..." -ForegroundColor Yellow

        try {
            # Create a new SSH session using New-PSSession
            $session = New-PSSession -HostName $ip -UserName $username -SSHTransport -Password $securePassword

            if ($session) {
                Write-Host "Connected to $ip. Running command..." -ForegroundColor Green

                # Run the command using Invoke-Command
                $output = Invoke-Command -Session $session -ScriptBlock { param($cmd) $cmd } -ArgumentList $command

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
        $results | Export-Csv -Path $csvOutputFile -NoTypeInformation -Force
        [System.Windows.Forms.MessageBox]::Show("Results have been written to $csvOutputFile", "Success", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Information)
    } catch {
        [System.Windows.Forms.MessageBox]::Show("Failed to write results to CSV file. Error: $_", "Error", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error)
    }
})
$form.Controls.Add($runButton)

# Show the form
$form.ShowDialog()
