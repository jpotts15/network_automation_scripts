import smtplib
import time
from datetime import datetime, timedelta
from ilo_control import HPEiLO  # Import the HPE iLO class from the first script

# iLO Connection Details
ILO_IP = "192.168.1.100"  # Replace with your iLO IP
ILO_USERNAME = "admin"  # Replace with your iLO username
ILO_PASSWORD = "password"  # Replace with your iLO password

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_email_password"  # Use an App Password if using Gmail
EMAIL_RECEIVER = "alert_email@example.com"

# OpenVPN Status File Path
OPENVPN_STATUS_FILE = "/etc/openvpn/status.log"

def send_email_alert(subject, message):
    """Send an email alert if the server is running when it shouldn't be."""
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)

        email_message = f"Subject: {subject}\n\n{message}"
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, email_message)
        server.quit()
        print(f"Email sent: {subject}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def get_openvpn_users():
    """Check if any OpenVPN users are currently online."""
    try:
        with open(OPENVPN_STATUS_FILE, "r") as file:
            lines = file.readlines()
            for line in lines:
                if "CLIENT_LIST" in line and "TCP" in line:
                    return True  # At least one user is connected
    except FileNotFoundError:
        print("OpenVPN status file not found.")
    return False  # No users online

def check_server():
    """Monitor the server's power state and determine if it should be on."""
    ilo = HPEiLO(ILO_IP, ILO_USERNAME, ILO_PASSWORD)
    ilo.connect()

    power_status = ilo.get_power_status()
    
    if power_status != "On":
        print("Server is already off. No action needed.")
        ilo.disconnect()
        return

    # Check how long the server has been on
    boot_time = ilo.session.get("/redfish/v1/Systems/1").dict.get("LastPowerOnTime")
    if boot_time:
        boot_time = datetime.strptime(boot_time, "%Y-%m-%dT%H:%M:%S%z")
        uptime = datetime.now().astimezone() - boot_time
    else:
        uptime = timedelta(hours=0)  # Assume recently started if boot time is unavailable

    print(f"Server has been on for {uptime}.")

    # Check OpenVPN users
    vpn_users_online = get_openvpn_users()

    # Get current time
    current_time = datetime.now()
    hour_now = current_time.hour

    # Decision Making
    if not vpn_users_online:
        if uptime > timedelta(hours=3):
            subject = "ALERT: Server has been on for too long with no VPN users!"
            message = f"The server has been running for {uptime}, but no OpenVPN users are online. Consider shutting it down."
            send_email_alert(subject, message)
        elif hour_now >= 23:  # After 11 PM
            subject = "ALERT: Server is running after 11 PM!"
            message = "The server is still running after 11 PM, but no OpenVPN users are connected."
            send_email_alert(subject, message)

    ilo.disconnect()

if __name__ == "__main__":
    while True:
        check_server()
        time.sleep(1800)  # Run every 30 minutes
