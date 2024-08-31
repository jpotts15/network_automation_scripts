<# Powershell API Checker GUI
Uses PS to check a API via GUI
Created by: Joseph Potts
Version 1.0
Last Update: 31Aug2024

To Run:
.\ps_api_checker_gui.ps1
#>

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Create the form
$form = New-Object System.Windows.Forms.Form
$form.Text = "Device API Checker"
$form.Size = New-Object System.Drawing.Size(400,300)
$form.StartPosition = "CenterScreen"

# Create labels and textboxes for API URL, Username, and Password/Token
$lblApiUrl = New-Object System.Windows.Forms.Label
$lblApiUrl.Text = "API URL:"
$lblApiUrl.Location = New-Object System.Drawing.Point(10,20)
$form.Controls.Add($lblApiUrl)

$txtApiUrl = New-Object System.Windows.Forms.TextBox
$txtApiUrl.Location = New-Object System.Drawing.Point(100, 20)
$txtApiUrl.Size = New-Object System.Drawing.Size(250,20)
$form.Controls.Add($txtApiUrl)

$lblUsername = New-Object System.Windows.Forms.Label
$lblUsername.Text = "Username:"
$lblUsername.Location = New-Object System.Drawing.Point(10,60)
$form.Controls.Add($lblUsername)

$txtUsername = New-Object System.Windows.Forms.TextBox
$txtUsername.Location = New-Object System.Drawing.Point(100, 60)
$txtUsername.Size = New-Object System.Drawing.Size(250,20)
$form.Controls.Add($txtUsername)

$lblPassword = New-Object System.Windows.Forms.Label
$lblPassword.Text = "Password/Token:"
$lblPassword.Location = New-Object System.Drawing.Point(10,100)
$form.Controls.Add($lblPassword)

$txtPassword = New-Object System.Windows.Forms.TextBox
$txtPassword.Location = New-Object System.Drawing.Point(100, 100)
$txtPassword.Size = New-Object System.Drawing.Size(250,20)
$txtPassword.UseSystemPasswordChar = $true
$form.Controls.Add($txtPassword)

# Create a button to trigger the API check
$btnCheckApi = New-Object System.Windows.Forms.Button
$btnCheckApi.Text = "Check API"
$btnCheckApi.Location = New-Object System.Drawing.Point(100, 140)
$form.Controls.Add($btnCheckApi)

# Create a textbox to display the results
$txtResult = New-Object System.Windows.Forms.TextBox
$txtResult.Location = New-Object System.Drawing.Point(10, 180)
$txtResult.Size = New-Object System.Drawing.Size(340,50)
$txtResult.Multiline = $true
$txtResult.ScrollBars = "Vertical"
$form.Controls.Add($txtResult)

# Define the function to check the device API
function CheckDeviceAPI {
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
        $EncodedAuth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("{$Username}:{$Password}"))
        $Headers = @{
            Authorization = "Basic $EncodedAuth"
        }
    }

    try {
        # Send a GET request to the API URL
        $Response = Invoke-RestMethod -Uri $ApiUrl -Headers $Headers -Method Get
        return "API request successful.`nResponse:`n$($Response | ConvertTo-Json -Depth 2)"
    } catch {
        return "Failed to connect to the API.`nError details:`n$($_.Exception.Message)"
    }
}

# Add an event handler to the button click event
$btnCheckApi.Add_Click({
    $ApiUrl = $txtApiUrl.Text
    $Username = $txtUsername.Text
    $Password = $txtPassword.Text

    # Clear previous results
    $txtResult.Text = ""

    # Call the function and display the result
    $Result = CheckDeviceAPI -ApiUrl $ApiUrl -Username $Username -Password $Password
    $txtResult.Text = $Result
})

# Show the form
$form.Topmost = $true
$form.Add_Shown({$form.Activate()})
[void]$form.ShowDialog()
