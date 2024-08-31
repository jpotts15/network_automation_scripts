"""
Python DNAC SDK API Example
Use the DNAC SDK to poke an API 
Created by: Joseph Potts
Version 1.0
Last Update: 31Aug2024

Requirements:
dnacentersdk

pip3 install dnacentersdk
python3 -m py_dnac_example_api_call.py
"""

from dnacentersdk import api

dnac = api.DNACenterAPI(base_url='https://sandboxdnac2.cisco.com:443',
username='devnetuser',password='Cisco123!')

devices = dnac.devices.get_device_list()
for device in devices.response:
    print(device.managementIpAddress)
