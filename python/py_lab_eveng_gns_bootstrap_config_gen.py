"""
Python Script to generate bootstrap configs for labs
Fill in the list/dict below

Created by: Joseph Potts
Version 1.0
Last Update: 31Aug2024

python3 -m py_lab_eveng_gns_bootstrap_config_gen.py.py

To Do:
1. fix that eigrp/ospf/isis apply configs to all ints
2. fix that eigrp/ospf/isis use the device ip instead of the subnet IP
3. Generate device list from other dict
4. Make this more DRY
5. Add tunneling generator
6. Integrate into a gns3/eveng automator to auto send configs

"""

import ipaddress


# Define the network layout
device_list = ["router1", "router2", "router3", "router4", "router5", "router6", "router7"]
connections = {
    "router1": {
        "interfaces": {
            "gi0/0": {"neighbor": "router2"},
            "gi0/1": {"neighbor": "router3"},
            "gi0/2": {"neighbor": "router4"}
        }
    },
    "router2": {
        "interfaces": {
            "gi0/0": {"neighbor": "router1"},
            "gi0/1": {"neighbor": "router6"},
            "gi0/3": {"neighbor": "router5"}
        }
    },
    "router3": {
        "interfaces": {
            "gi0/1": {"neighbor": "router1"},
            "gi0/0": {"neighbor": "router4"},
            "gi0/3": {"neighbor": "router6"}
        }
    },
    "router4": {
        "interfaces": {
            "gi0/2": {"neighbor": "router1"},
            "gi0/0": {"neighbor": "router3"},
            "gi0/3": {"neighbor": "router7"}
        }
    },
    "router5": {
        "interfaces": {
            "gi0/3": {"neighbor": "router2"},
            "gi0/0": {"neighbor": "router7"}
        }
    },
    "router6": {
        "interfaces": {
            "gi0/1": {"neighbor": "router2"},
            "gi0/3": {"neighbor": "router3"}
        }
    },
    "router7": {
        "interfaces": {
            "gi0/0": {"neighbor": "router5"},
            "gi0/3": {"neighbor": "router4"}
        }
    }
}

base_ip_range = "10.0.0.0/16"
default_interface_mask = "/30"
base_configs = [
    'ip domain-name lt-networks.com',
    'crypto key generate rsa modulus 2048',
    'username test privilege 15 password test',
    'line vty 0 15',
    'login local'
]

# New dictionaries for BGP, OSPF, EIGRP, and ISIS
bgp_neighbors = {
    "ebgp": {
        "router1": {"neighbors": {"router2": "router1", "router3": "router1", "router4": "router1"}, "asn": 65000},
        "router2": {"neighbors": {"router1": "router2"}, "asn": 65001},
        "router3": {"neighbors": {"router1": "router2"}, "asn": 65002},
        "router4": {"neighbors": {"router1": "router2"}, "asn": 65002}
    },
    "ibgp": {

    }
}

ospf_areas = {
    0: {"devices": ["router2", "router5"]}
}

isis_areas = {
    "l1l2": {"devices": ["router3", "router6"]}
}

eigrp_neighbors = {
    1: {"devices": ["router4", "router7"]}
}

def generate_ip_subnet(base_ip, subnet_index):
    subnet = ipaddress.ip_network(base_ip).subnets(new_prefix=int(default_interface_mask.strip('/')))
    return list(subnet)[subnet_index]

def generate_interface_ips(device_list, connections, base_ip_range):
    ip_subnets = {}
    interface_details = {}
    subnet_index = 0

    for device in device_list:
        if device not in interface_details:
            interface_details[device] = {}

        for interface, details in connections[device]["interfaces"].items():
            neighbor = details["neighbor"]

            # Generate and assign IP subnet if not already done
            if (device, neighbor) not in ip_subnets and (neighbor, device) not in ip_subnets:
                ip_subnets[(device, neighbor)] = generate_ip_subnet(base_ip_range, subnet_index)
                subnet_index += 1

            ip_subnet = ip_subnets[(device, neighbor)] if (device, neighbor) in ip_subnets else ip_subnets[(neighbor, device)]
            ips = list(ip_subnet.hosts())
            interface_details[device][interface] = {'ip': ips[0], 'mask': ip_subnet.netmask}

            # Ensure neighbor interface is also recorded
            if neighbor not in interface_details:
                interface_details[neighbor] = {}
            neighbor_interface = next(k for k, v in connections[neighbor]["interfaces"].items() if v["neighbor"] == device)
            interface_details[neighbor][neighbor_interface] = {'ip': ips[1], 'mask': ip_subnet.netmask}

    return interface_details

def generate_base_configs(device):
    config_lines = [f"hostname {device}"]
    config_lines.extend(base_configs)
    return config_lines

def generate_interface_configs(device, connections, interface_details):
    config_lines = []
    for interface, details in interface_details[device].items():
        ip = details['ip']
        mask = details['mask']
        config_lines.append(f"interface {interface}")
        config_lines.append(f" ip address {ip} {mask}")
        config_lines.append(" no shutdown")
    return config_lines

def generate_ospf_configs(device, ospf_areas, interface_details, connections):
    config_lines = []
    for area, area_details in ospf_areas.items():
        if device in area_details["devices"]:
            config_lines.append(f"router ospf 1")
            for interface, details in interface_details[device].items():
                if interface in connections[device]["interfaces"]:  # Check if interface should participate in OSPF
                    ip = details['ip']
                    mask = details['mask']
                    wildcard_mask = str(ipaddress.IPv4Address(int(ipaddress.IPv4Address('255.255.255.255')) ^ int(mask)))
                    config_lines.append(f" network {ip} {wildcard_mask} area {area}")
    return config_lines


def generate_eigrp_configs(device, eigrp_neighbors, interface_details, connections):
    config_lines = ["no auto-summary"]
    for eigrp_as, area_details in eigrp_neighbors.items():
        if device in area_details["devices"]:
            config_lines.insert(0, f"router eigrp {eigrp_as}")
            for interface, details in interface_details[device].items():
                if interface in connections[device]["interfaces"]:  # Check if interface should participate in EIGRP
                    ip = details['ip']
                    mask = details['mask']
                    wildcard_mask = str(ipaddress.IPv4Address(int(ipaddress.IPv4Address('255.255.255.255')) ^ int(mask)))
                    config_lines.append(f" network {ip} {wildcard_mask}")
    return config_lines


# Function to generate BGP configurations
def generate_bgp_configs(device, bgp_neighbors, ip_addresses):
    config_lines = ["no auto-summary"]
    for neighbor_type, devices in bgp_neighbors.items():
        if device in devices:
            asn = devices[device]["asn"]
            config_lines.insert(0, f"router bgp {asn}")
            for neighbor in devices[device]["neighbors"]:
                neighbor_ip = ip_addresses[neighbor][next(k for k, v in connections[neighbor]["interfaces"].items() if v["neighbor"] == device)]['ip']
                neighbor_asn = bgp_neighbors[neighbor_type][neighbor]["asn"]
                config_lines.append(f" neighbor {neighbor_ip} remote-as {neighbor_asn}")
    return config_lines

def isis_id_gen(ipv4_ip):
    # generate a CLNP net address for ISIS ID
    ipv4_ip = str(ipaddress.IPv4Address(ipv4_ip))
    ipv4_ip_parsed = ""
    for octet in ipv4_ip.split('.'):
        if len(octet) == 1:
            octet = "00" + octet 
        elif len(octet) == 2:
            octet = "0" + octet
        ipv4_ip_parsed += octet
    ipv4_ip_parsed = f"{ipv4_ip_parsed[0:4]}.{ipv4_ip_parsed[4:8]}.{ipv4_ip_parsed[8:]}"
    return f'49.0001.{ipv4_ip_parsed}.00'

def generate_isis_configs(device, isis_areas, interface_details, connections):
    config_lines = []
    for area, area_details in isis_areas.items():
        if device in area_details["devices"]:
            isis_id = isis_id_gen(list(interface_details[device].values())[0]['ip'])
            config_lines.insert(0, f"router isis")
            config_lines.insert(1, f"net {isis_id}")
            for interface, details in interface_details[device].items():
                if interface in connections[device]["interfaces"]:  # Check if interface should participate in ISIS
                    config_lines.append(f"interface {interface}")
                    config_lines.append(f" ip router isis")
    return config_lines


def generate_configs(device_list, connections, base_ip_range, base_configs, bgp_neighbors, ospf_areas):
    interface_details = generate_interface_ips(device_list, connections, base_ip_range)
    device_configs = {}

    for device in device_list:
        if device not in device_configs:
            base_config_lines = generate_base_configs(device)
            interface_config_lines = generate_interface_configs(device, connections, interface_details)
            ospf_config_lines = generate_ospf_configs(device, ospf_areas, interface_details, connections)
            bgp_config_lines = generate_bgp_configs(device, bgp_neighbors, interface_details)
            eigrp_config_lines = generate_eigrp_configs(device, eigrp_neighbors, interface_details, connections)
            isis_config_lines = generate_isis_configs(device, isis_areas, interface_details, connections)
            config_lines = base_config_lines + interface_config_lines + ospf_config_lines + bgp_config_lines + eigrp_config_lines + isis_config_lines
            device_configs[device] = '\n'.join(config_lines) + '\n'

    return device_configs

def save_configs(configs):
    for device, config in configs.items():
        with open(f"{device}_config.txt", "w") as file:
            file.write(config)
        print(f"Configuration for {device}: ")
        print(config)
        print(f"Configuration for {device} has been written to {device}_config.txt")

# Load, generate, and save configurations
configs = generate_configs(device_list, connections, base_ip_range, base_configs, bgp_neighbors, ospf_areas)
save_configs(configs)