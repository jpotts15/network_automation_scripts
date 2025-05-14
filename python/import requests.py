import requests
import json
from datetime import datetime, timedelta

# Configuration
SOLARWINDS_API_URL = "https://your-solarwinds-server:17778/SolarWinds/InformationService/v3/Json/Query"
SOLARWINDS_UPDATE_API_URL = "https://your-solarwinds-server:17778/SolarWinds/InformationService/v3/Json/Invoke"
SOLARWINDS_USERNAME = "your_username"
SOLARWINDS_PASSWORD = "your_password"
SPLUNK_HEC_URL = "https://your-splunk-server:8088/services/collector"
SPLUNK_TOKEN = "your_splunk_token"

# Disable SSL warnings (if using self-signed certs)
requests.packages.urllib3.disable_warnings()

def get_nodes():
    """Fetches the list of nodes from SolarWinds."""
    query = "SELECT NodeID, Caption FROM Orion.Nodes"
    response = requests.post(
        SOLARWINDS_API_URL,
        auth=(SOLARWINDS_USERNAME, SOLARWINDS_PASSWORD),
        json={"query": query},
        verify=False
    )
    response.raise_for_status()
    return response.json().get("results", [])

def get_node_status(node_id):
    """Fetches the status of a given node from SolarWinds."""
    query = f"SELECT Status FROM Orion.Nodes WHERE NodeID={node_id}"
    response = requests.post(
        SOLARWINDS_API_URL,
        auth=(SOLARWINDS_USERNAME, SOLARWINDS_PASSWORD),
        json={"query": query},
        verify=False
    )
    response.raise_for_status()
    results = response.json().get("results", [])
    return results[0]["Status"] if results else "Unknown"

def get_interfaces(node_id):
    """Fetches all interfaces for a given node and their statuses."""
    query = f"SELECT InterfaceID, InterfaceName, Status, AdminStatus, LastChange FROM Orion.NPM.Interfaces WHERE NodeID={node_id}"
    response = requests.post(
        SOLARWINDS_API_URL,
        auth=(SOLARWINDS_USERNAME, SOLARWINDS_PASSWORD),
        json={"query": query},
        verify=False
    )
    response.raise_for_status()
    return response.json().get("results", [])

def filter_old_interfaces(interfaces):
    """Filters interfaces that are up/down and haven't changed in the last 6 months."""
    six_months_ago = datetime.utcnow() - timedelta(days=180)
    old_interfaces = []
    
    for interface in interfaces:
        last_change = interface.get("LastChange")
        if last_change:
            last_change_date = datetime.strptime(last_change, "%Y-%m-%dT%H:%M:%S")
            if last_change_date < six_months_ago:
                old_interfaces.append(interface)
    
    return old_interfaces

def disable_interface(interface_id):
    """Disables an interface in SolarWinds."""
    payload = {
        "query": "Orion.NPM.Interfaces::Unmanage",
        "parameters": {
            "netObjectId": f"I:{interface_id}",
            "unmanageTime": datetime.utcnow().isoformat() + "Z",
            "remanageTime": (datetime.utcnow() + timedelta(days=365)).isoformat() + "Z",
            "isRelative": False
        }
    }
    response = requests.post(
        SOLARWINDS_UPDATE_API_URL,
        auth=(SOLARWINDS_USERNAME, SOLARWINDS_PASSWORD),
        json=payload,
        verify=False
    )
    response.raise_for_status()
    print(f"Interface {interface_id} disabled successfully.")

def get_hardware_sensors(node_id):
    """Fetches hardware sensors for a given node."""
    query = f"SELECT ID, Name, Status FROM Orion.HardwareHealth.HardwareItem WHERE NodeID={node_id}"
    response = requests.post(
        SOLARWINDS_API_URL,
        auth=(SOLARWINDS_USERNAME, SOLARWINDS_PASSWORD),
        json={"query": query},
        verify=False
    )
    response.raise_for_status()
    return response.json().get("results", [])

def disable_hardware_sensor(sensor_id):
    """Disables a hardware sensor in SolarWinds."""
    payload = {
        "query": "Orion.HardwareHealth.HardwareItem::DisableSensors",
        "parameters": {
            "ID": sensor_id
        }
    }
    response = requests.post(
        SOLARWINDS_UPDATE_API_URL,
        auth=(SOLARWINDS_USERNAME, SOLARWINDS_PASSWORD),
        json=payload,
        verify=False
    )
    response.raise_for_status()
    print(f"Hardware sensor {sensor_id} disabled successfully.")

def process_interfaces_and_sensors(node_id):
    """Processes interfaces and disables associated hardware sensors if needed."""
    interfaces = get_interfaces(node_id)
    sensors = get_hardware_sensors(node_id)
    
    for interface in interfaces:
        if interface["AdminStatus"] == 0:  # Admin down
            for sensor in sensors:
                if "Current Sensor" in sensor["Name"] or "Receive Power Sensor" in sensor["Name"]:
                    disable_hardware_sensor(sensor["ID"])

def send_to_splunk(data):
    """Sends the collected node and interface data to Splunk."""
    headers = {
        "Authorization": f"Splunk {SPLUNK_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "event": data,
        "sourcetype": "_json"
    }
    response = requests.post(SPLUNK_HEC_URL, headers=headers, json=payload, verify=False)
    response.raise_for_status()
    print("Data sent to Splunk successfully.")

def main():
    """Main function to get nodes, fetch statuses, interfaces, and push to Splunk."""
    nodes = get_nodes()
    
    for node in nodes:
        node_id = node["NodeID"]
        caption = node["Caption"]
        status = get_node_status(node_id)
        interfaces = get_interfaces(node_id)
        old_interfaces = filter_old_interfaces(interfaces)
        
        for interface in old_interfaces:
            disable_interface(interface["InterfaceID"])
        
        process_interfaces_and_sensors(node_id)
        
        node_data = {
            "NodeID": node_id,
            "Caption": caption,
            "Status": status,
            "Interfaces": interfaces,
            "OldInterfaces": old_interfaces
        }
        
        print(f"Sending: {node_data}")
        send_to_splunk(node_data)
    
if __name__ == "__main__":
    main()
