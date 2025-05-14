import redfish
import redfish.rest
import sys
from os import sleep

# iLO Connection Details
ILO_IP = "192.168.178.7"  # Replace with your iLO IP address
ILO_USERNAME = "api_user"  # Replace with your iLO username
ILO_PASSWORD = "!NFnfna*#nQFN154"  # Replace with your iLO password

class HPEiLO:
    def __init__(self, ilo_ip, username, password):
        """Initialize connection to HPE iLO"""
        self.ilo_ip = ilo_ip
        self.username = username
        self.password = password
        self.base_url = f"https://{ilo_ip}"
        self.session = None

    def connect(self):
        """Establish a Redfish session"""
        try:
            self.session = redfish.redfish_client(base_url=self.base_url, username=self.username, password=self.password)
            self.session.login(auth="session")
            print("Connected to HPE iLO successfully.")
        except Exception as e:
            print(f"Failed to connect to iLO: {e}")
            sys.exit(1)

    def disconnect(self):
        """Logout and close session"""
        if self.session:
            self.session.logout()
            print("Disconnected from HPE iLO.")

    def get_power_status(self):
        """Retrieve the server power status"""
        response = self.session.get("/redfish/v1/Systems/1")
        if response.status == 200:
            power_state = response.dict["PowerState"]
            print(f"Current Power State: {power_state}")
            return power_state
        else:
            print(f"Failed to get power status: {response.status}")
            return None

    def power_on(self):
        """Power on the server"""
        print("Attempting to power on the server...")
        power_state = self.get_power_status()
        if power_state == "On":
            print("Server is already powered on.")
            return

        body = {"Action": "Reset", "ResetType": "On"}
        response = self.session.post("/redfish/v1/Systems/1/Actions/ComputerSystem.Reset", body=body)
        if response.status == 200:
            print("Powering on the server successfully.")
        else:
            print(f"Failed to power on the server: {response.status}")

    def power_off(self):
        """Power off the server"""
        print("Attempting to power off the server gracefully...")
        power_state = self.get_power_status()
        if power_state == "Off":
            print("Server is already powered off.")
            return

        body = {"Action": "Reset", "ResetType": "GracefulShutdown"}
        response = self.session.post("/redfish/v1/Systems/1/Actions/ComputerSystem.Reset", body=body)
        if response.status == 200:
            print("Graceful shutdown sent to server successfully, will wait 30 second and start the check loop...")
        else:
            print(f"Failed to power off the server: {response.status}")
        # double check power status,
        sleep(30)
        power_state = self.get_power_status()
        retry_counter = 0
        powering_off_counter = 0
        while power_state != "Off" and retry_counter < 4:
            power_state = self.get_power_status()
            if power_state == None:
                print("API for powercheck failed, going to retry in 10 seconds")
                retry_counter += 1
                sleep(10)
                continue
            elif power_state == "PoweringOff":
                if powering_off_counter < 13:
                    print("server still showing powering off, waiting 10 seconds and rechecking")
                    sleep(10)
                    powering_off_counter += 1
                else:
                    print("waited too long, going to ForceOff")
                    body = {"Action": "Reset", "ResetType": "ForceOff"}
                    response = self.session.post("/redfish/v1/Systems/1/Actions/ComputerSystem.Reset", body=body)
                    if response.status == 200:
                        print("Powering off the server successfully.")
                    else:
                        print(f"Failed to power off the server: {response.status}")
            else:
                print("Graceful shutdown complete")
        return f"server state: {self.get_power_status()}"
