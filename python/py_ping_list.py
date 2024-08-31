"""
Ping a list of IPs from CSV

Created by: Joseph Potts
Version 1.0
Last Update: 31Aug2024

# Example usage
input_csv_file = 'input_ips.csv'
output_csv_file = 'output_status.csv'
process_ips(input_csv_file, output_csv_file)
"""

import csv
import subprocess
import platform

def ping_ip(ip_address):
    # Determine the OS since flags differ from windows to *nix
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', ip_address]

    try:
        # Run the ping command
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def process_ips(input_csv, output_csv):
    # Open the input CSV file for reading
    with open(input_csv, mode='r') as infile:
        reader = csv.DictReader(infile)
        
        # Prepare to write to the output CSV file
        with open(output_csv, mode='w', newline='') as outfile:
            fieldnames = ['IP', 'Status']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            
            writer.writeheader()
            
            for row in reader:
                ip = row['IP']
                status = 'Reachable' if ping_ip(ip) else 'Unreachable'
                writer.writerow({'IP': ip, 'Status': status})