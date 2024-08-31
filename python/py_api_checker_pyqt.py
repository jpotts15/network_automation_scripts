"""
Python function to check an api with pyqt frontend

Created by: Joseph Potts
Version 1.0
Last Update: 31Aug2024

# Example usage:
python3 -m py_api_checker_pyqt.py
"""

import sys
import requests
from requests.auth import HTTPBasicAuth
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QTextEdit

def call_api(api_url, username, password):
    """
    Calls the API with the given URL, username, and password.
    """
    if username == "token":
        headers = {
            "Authorization": f"Token {password}"
        }
        response = requests.get(api_url, headers=headers)
    else:
        response = requests.get(api_url, auth=HTTPBasicAuth(username, password))
    
    return response

class ApiCallerApp(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the UI
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('API Caller')

        # Create widgets
        self.url_input = QLineEdit(self)
        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.submit_button = QPushButton('Submit', self)
        self.result_output = QTextEdit(self)
        self.result_output.setReadOnly(True)

        # Create layout
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        form_layout.addRow('API URL:', self.url_input)
        form_layout.addRow('Username:', self.username_input)
        form_layout.addRow('Password/Token:', self.password_input)
        layout.addLayout(form_layout)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.result_output)

        self.setLayout(layout)

        # Connect button click event
        self.submit_button.clicked.connect(self.on_submit)

    def on_submit(self):
        api_url = self.url_input.text()
        username = self.username_input.text()
        password = self.password_input.text()

        if not api_url or not username or not password:
            self.result_output.setText("Please fill in all fields.")
            return

        try:
            response = call_api(api_url, username, password)
            if response.ok:
                self.result_output.setText(f"Response Data:\n{response.json()}")
            else:
                self.result_output.setText(f"Error: {response.status_code}\n{response.text}")
        except Exception as e:
            self.result_output.setText(f"Exception occurred: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ApiCallerApp()
    window.show()
    sys.exit(app.exec_())
