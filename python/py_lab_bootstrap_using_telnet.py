"""
EVENG Lab Boot strapper using telnet
Modify the script for your eveng details and the telnet start port and number of devices (assumes incremental telnet ports).
This uses a custom telnet lib due to the python standard telnet lib being depcreiated 
Created by: Joseph Potts
Version 1.0
Last Update: 31Aug2024

python3 -m py_lab_bootstrap_using_telnet.py
"""

import python.py_telnet_holdover as py_telnet_holdover
from getpass import getpass
from time import sleep

host_dict = {1: {'ip':"172.24.177.49", "telnet_port": 32777}
             # 2: {'ip':"172.24.177.49", "telnet_port": 32800},
             # 3: {'ip':"172.24.177.49", "telnet_port": 32801},
             # 4: {'ip':"172.24.177.49", "telnet_port": 32802},
             # 5: {'ip':"172.24.177.49", "telnet_port": 32803},
             # 6: {'ip':"172.24.177.49", "telnet_port": 32804}
             }

commands_to_send =["en", "conf t", "int range et0/0 - 3, et1/0 - 3, et2/0 - 3, et3/0 - 3","shut", "int range et4/0 - 3, et5/0 - 3, et6/0 - 3",
                   "shut","vlan 10","vlan 20","vlan 30","vlan 40", "end"]

eveng_host = "172.24.177.49"
port_start = 32777
num_devices = 1

for port in range(num_devices):
    print(f"Sending to host {eveng_host}, port {port_start + port}")
    tn = py_telnet_holdover.Telnet(eveng_host, port_start + port)
    prompt_decoder = False
    loop_counter = 0
    while prompt_decoder != True or loop_counter < 10:
        loop_counter += 1
        tn.write(b"\r\n")
        prompt = tn.read_until(b">", 1).decode("ascii")
        if ">" in prompt:
            tn.write(b"en\r\n")
            prompt = tn.read_until(b"#", 1).decode("ascii")
        elif "(confi" in prompt:
            tn.write(b"end\r\n")
        elif "#" in prompt:
            tn.write(b"term len 0\r\n")
            prompt_decoder = True
            #print("user exec mode")
            break
        elif "initial configuration" or "Please answer" in prompt:
            #print("setup mode")
            tn.write(b"no\r\n")
            tn.write(b"\r\n")
    tn.write(b"\r\n")
    for command in commands_to_send:
        printer = tn.read_until(b"#")  # Adjust the expected prompt accordingly
        tn.write(command.encode('ascii') + b"\r\n")
    sleep(1)
    tn.write(b"end\r\n")
    tn.write(b"term len 60\r\n")
    tn.write(b"exit\r\n")
    output = tn.read_very_eager()
    print(output.decode())
    print("Sending complete!")
    tn.close()
