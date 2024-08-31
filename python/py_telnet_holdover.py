"""
Python Telnet Implimentation using sockets
WARNING: Don't use in production as telnet is insecure, should only be used for testing/ lab enviorments
Created by: Joseph Potts
Version 1.0
Last Update: 31Aug2024
"""


import socket
import selectors
import time

class Telnet:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.create_connection((host, port))
        self.selector = selectors.DefaultSelector()
        self.selector.register(self.sock, selectors.EVENT_READ)

    def send_command(self, command):
        self.sock.sendall(command.encode('utf-8'))

    def receive_response(self):
        data = self.sock.recv(65536)
        return data

    def receive_response_all(self):
        self.sock.setblocking()

    def close(self):
        self.sock.close()

class CiscoTelnet:
    def __init__(self, host, port, username, password):
        self.telnet = Telnet(host, port)
        self.username = username
        self.password = password

    def prompt_identifier(self):
        raw_prompt = self._read_raw_prompt()
        self._send_command('\r\n')
        time.sleep(1)
        raw_prompt = self._read_raw_prompt()
        # grab the new prompt
        prompt = raw_prompt.decode('utf-8')
        return prompt

    def _send_command(self, command):
        self.telnet.send_command(command + '\r\n')

    def _read_raw_prompt(self):
        return self.telnet.receive_response()

    def login(self):
        prompt = self.prompt_identifier()
        retry_counter = 0
        while "#" not in prompt and retry_counter < 5:
            retry_counter += 1
            if "initial" in prompt.lower() or "yes/no" in prompt.lower():
                self._send_command("no")
                time.sleep(30)
                self.prompt_identifier()  # Update prompt after 'no' command

            elif "username" in prompt.lower():
                self._send_command(self.username)
                time.sleep(1)
                self._send_command(self.password)
                self.prompt_identifier()  # Update prompt after login

            elif ">" in prompt:
                self._send_command("en")
                time.sleep(1)
                prompt = self.prompt_identifier()  # Update prompt after 'en' command

    def cisco_send_command(self, command):
        self._send_command(command)
        prompt = self.prompt_identifier()
        time.sleep(1)
        return prompt

    def close(self):
        self.telnet.close()
