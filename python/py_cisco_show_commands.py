"""
Cisco Show commands using Netmiko
Python netmiko script to ssh to a a list of devices and run some show commands
Created by: Joseph Potts
Version 1.0
Last Update: 31Aug2024

Requirements:
netmiko

pip3 install netmiko getpass
python3 -m py_cisco_show_commands.py
"""

from netmiko import ConnectHandler
from getpass import getpass

def connect_to_device(device_ip, username, password, device_type='cisco_ios'):
    """
    Connect to a network device using Netmiko.

    :param device_ip: IP address of the network device
    :param username: Username for authentication
    :param password: Password for authentication
    :param device_type: Type of the network device (default is 'cisco_ios')
    :return: Netmiko SSH session object
    """
    device = {
        'device_type': device_type,
        'ip': device_ip,
        'username': username,
        'password': password,
        'secret': password,  # Enable password (if applicable)
        'verbose': True,
    }

    try:
        net_connect = ConnectHandler(**device)
        print(f"Connected to {device_ip}")
        return net_connect
    except Exception as e:
        print(f"Failed to connect to {device_ip}: {e}")
        return None

def run_show_commands(net_connect, commands):
    """
    Run a list of show commands on the network device.

    :param net_connect: Netmiko SSH session object
    :param commands: List of show commands to run
    """
    try:
        for command in commands:
            output = net_connect.send_command(command)
            print(f"Command: {command}\n{output}\n{'='*50}")
    except Exception as e:
        print(f"Failed to run show commands: {e}")

def disconnect_from_device(net_connect):
    """
    Disconnect from the network device.

    :param net_connect: Netmiko SSH session object
    """
    net_connect.disconnect()
    print("Disconnected from the device.")

ip_list = ["172.20.49.244","172.20.49.245"]
command_list = ["show ip int bri"]

# execute above
user = input('Enter your username: ')
pw = getpass('Enter password: ')
for ip in ip_list:
    con1 = connect_to_device(ip,user,pw)
    run_show_commands(con1,command_list)
    disconnect_from_device(con1)
