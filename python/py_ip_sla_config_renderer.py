"""
Python IP SLA config renderer with pyqt5 frontend
Created by: Joseph Potts
Version 1.0
Last Update: 22Sept2024

python3 -m py_ip_sla_config_renderer.py
"""

from PyQt5 import QtWidgets, QtGui
from jinja2 import Template
import sys
import csv

class IPSLAGeneratorApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Top-level radio options
        self.input_mode_label = QtWidgets.QLabel('Input Mode:')
        self.input_mode_manual = QtWidgets.QRadioButton('Manual Input')
        self.input_mode_csv = QtWidgets.QRadioButton('CSV Input')
        self.input_mode_manual.setChecked(True)
        self.input_mode_manual.toggled.connect(self.toggle_input_mode)

        # Create UI elements for manual input
        self.ip_sla_label = QtWidgets.QLabel('IP SLA Number:')
        self.ip_sla_num = QtWidgets.QLineEdit()

        self.device1_ip_label = QtWidgets.QLabel('Device 1 IP:')
        self.device1_ip_input = QtWidgets.QLineEdit()

        self.device2_ip_label = QtWidgets.QLabel('Device 2 IP:')
        self.device2_ip_input = QtWidgets.QLineEdit()

        self.sla_type_label = QtWidgets.QLabel('IP SLA Type:')
        self.sla_type_dropdown = QtWidgets.QComboBox()
        self.sla_type_dropdown.addItems(['icmp-echo', 'icmp-jitter', 'udp-echo_sla', 'tcp'])
        self.sla_type_dropdown.currentTextChanged.connect(self.toggle_port_field)

        self.port_label = QtWidgets.QLabel('Port:')
        self.port_input = QtWidgets.QLineEdit()
        self.port_label.setVisible(False)
        self.port_input.setVisible(False)

        self.threshold_label = QtWidgets.QLabel('Threshold (ms):')
        self.threshold_input = QtWidgets.QLineEdit()

        self.freq_label = QtWidgets.QLabel('Frequency (s):')
        self.freq_input = QtWidgets.QLineEdit()

        # Create UI elements for CSV input
        self.csv_file_label = QtWidgets.QLabel('CSV File:')
        self.csv_file_input = QtWidgets.QLineEdit()
        self.csv_browse_button = QtWidgets.QPushButton('Browse')
        self.csv_browse_button.clicked.connect(self.browse_csv)
        self.csv_file_label.setVisible(False)
        self.csv_file_input.setVisible(False)
        self.csv_browse_button.setVisible(False)

        self.save_location_label = QtWidgets.QLabel('Save Location:')
        self.save_location_input = QtWidgets.QLineEdit()
        self.save_button = QtWidgets.QPushButton('Browse')
        self.save_button.clicked.connect(self.browse_file)

        self.generate_button = QtWidgets.QPushButton('Generate')
        self.generate_button.clicked.connect(self.generate_config)

        self.output_display = QtWidgets.QTextEdit()
        self.output_display.setReadOnly(True)

        # Layout setup
        grid = QtWidgets.QGridLayout()
        grid.addWidget(self.input_mode_label, 0, 0)
        grid.addWidget(self.input_mode_manual, 0, 1)
        grid.addWidget(self.input_mode_csv, 0, 2)
        
        grid.addWidget(self.ip_sla_label, 1, 0)
        grid.addWidget(self.ip_sla_num, 1, 1)
        grid.addWidget(self.device1_ip_label, 2, 0)
        grid.addWidget(self.device1_ip_input, 2, 1)
        grid.addWidget(self.device2_ip_label, 3, 0)
        grid.addWidget(self.device2_ip_input, 3, 1)
        grid.addWidget(self.sla_type_label, 4, 0)
        grid.addWidget(self.sla_type_dropdown, 4, 1)
        grid.addWidget(self.port_label, 5, 0)
        grid.addWidget(self.port_input, 5, 1)
        grid.addWidget(self.threshold_label, 6, 0)
        grid.addWidget(self.threshold_input, 6, 1)
        grid.addWidget(self.freq_label, 7, 0)
        grid.addWidget(self.freq_input, 7, 1)

        grid.addWidget(self.csv_file_label, 8, 0)
        grid.addWidget(self.csv_file_input, 8, 1)
        grid.addWidget(self.csv_browse_button, 8, 2)

        grid.addWidget(self.save_location_label, 9, 0)
        grid.addWidget(self.save_location_input, 9, 1)
        grid.addWidget(self.save_button, 9, 2)
        grid.addWidget(self.generate_button, 10, 0, 1, 3)
        grid.addWidget(self.output_display, 11, 0, 1, 3)

        self.setLayout(grid)
        self.setWindowTitle('Cisco IP SLA Config Generator')
        self.show()

    def toggle_port_field(self, text):
        if text in ['udp', 'tcp']:
            self.port_label.setVisible(True)
            self.port_input.setVisible(True)
        else:
            self.port_label.setVisible(False)
            self.port_input.setVisible(False)

    def toggle_input_mode(self):
        if self.input_mode_csv.isChecked():
            self.ip_sla_label.setVisible(False)
            self.ip_sla_num.setVisible(False)
            self.device1_ip_label.setVisible(False)
            self.device1_ip_input.setVisible(False)
            self.device2_ip_label.setVisible(False)
            self.device2_ip_input.setVisible(False)
            self.sla_type_label.setVisible(False)
            self.sla_type_dropdown.setVisible(False)
            self.port_label.setVisible(False)
            self.port_input.setVisible(False)
            self.threshold_label.setVisible(False)
            self.threshold_input.setVisible(False)
            self.freq_label.setVisible(False)
            self.freq_input.setVisible(False)
            self.csv_file_label.setVisible(True)
            self.csv_file_input.setVisible(True)
            self.csv_browse_button.setVisible(True)
        else:
            self.ip_sla_label.setVisible(True)
            self.ip_sla_num.setVisible(True)
            self.device1_ip_label.setVisible(True)
            self.device1_ip_input.setVisible(True)
            self.device2_ip_label.setVisible(True)
            self.device2_ip_input.setVisible(True)
            self.sla_type_label.setVisible(True)
            self.sla_type_dropdown.setVisible(True)
            self.threshold_label.setVisible(True)
            self.threshold_input.setVisible(True)
            self.freq_label.setVisible(True)
            self.freq_input.setVisible(True)
            self.csv_file_label.setVisible(False)
            self.csv_file_input.setVisible(False)
            self.csv_browse_button.setVisible(False)

    def browse_file(self):
        save_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '', 'Text Files (*.txt);;All Files (*)')
        if save_path:
            self.save_location_input.setText(save_path)

    def browse_csv(self):
        csv_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open CSV File', '', 'CSV Files (*.csv);;All Files (*)')
        if csv_path:
            self.csv_file_input.setText(csv_path)

    def generate_config(self):
        save_location = self.save_location_input.text()

        if self.input_mode_manual.isChecked():
            ip_sla_num = self.ip_sla_num.text() or "1"
            device1_ip = self.device1_ip_input.text()
            device2_ip = self.device2_ip_input.text()
            sla_type = self.sla_type_dropdown.currentText()
            threshold = self.threshold_input.text()
            frequency = self.freq_input.text()
            port = self.port_input.text() if sla_type in ['udp', 'tcp'] else None

            # Validate input
            if not device1_ip or not device2_ip:
                self.output_display.setText('Please fill in all required fields.')
                return

            # Jinja2 template
            template_str = """
            ip sla {{ ip_sla_num }}
             {{ sla_type }} {{ device_ip }}{% if port %} port {{ port }}{% endif %}
             threshold {{ threshold }}
             frequency {{ frequency }}
            ip sla schedule {{ ip_sla_num }} life forever start-time now
            """

            template = Template(template_str)
            config1 = template.render(ip_sla_num=ip_sla_num, device_ip=device2_ip, sla_type=sla_type, threshold=threshold, frequency=frequency, port=port)
            config2 = template.render(ip_sla_num=ip_sla_num, device_ip=device1_ip, sla_type=sla_type, threshold=threshold, frequency=frequency, port=port)
            config = f"\n# Device 1\n{config1}\n\n# Device 2\n{config2}"

            # Display and save output
            self.output_display.setText(config)
            if save_location:
                try:
                    with open(save_location, 'w') as file:
                        file.write(config)
                except Exception as e:
                    self.output_display.setText(f'Error saving file: {e}')

        elif self.input_mode_csv.isChecked():
            csv_file = self.csv_file_input.text()
            if not csv_file:
                self.output_display.setText('Please provide a CSV file.')
                return

            output = ""
            ip_sla_num = 1
            try:
                with open(csv_file, 'r') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        device1_ip = row.get('device1_ip', '')
                        device2_ip = row.get('device2_ip', '')
                        sla_type = row.get('sla_type', '')
                        threshold = row.get('threshold', '')
                        frequency = row.get('frequency', '')
                        port = row.get('port', None)
                        if row.get('ip_sla_num') != "":
                            sla_num = row.get('ip_sla_num', ip_sla_num)
                        elif sla_num:
                            sla_num = int(sla_num) + 1
                        else:
                            sla_num = 1

                        
                        # Generate config
                        template_str = """
                        ip sla {{ ip_sla_num }}
                         {{ sla_type }} {{ device_ip }}{% if port %} port {{ port }}{% endif %}
                         threshold {{ threshold }}
                         frequency {{ frequency }}
                        ip sla schedule {{ ip_sla_num }} life forever start-time now
                        """
                        template = Template(template_str)
                        config1 = template.render(ip_sla_num=sla_num, device_ip=device2_ip, sla_type=sla_type, threshold=threshold, frequency=frequency, port=port)
                        config2 = template.render(ip_sla_num=sla_num, device_ip=device1_ip, sla_type=sla_type, threshold=threshold, frequency=frequency, port=port)
                        output += f"\n# Device 1\n{config1}\n\n# Device 2\n{config2}\n"
                        
                        ip_sla_num += 1

                self.output_display.setText(output)
                if save_location:
                    with open(save_location, 'w') as file:
                        file.write(output)
            except Exception as e:
                self.output_display.setText(f'Error processing CSV: {e}')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = IPSLAGeneratorApp()
    sys.exit(app.exec_())