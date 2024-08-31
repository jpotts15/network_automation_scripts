from jinja2 import Environment, FileSystemLoader
import os

# Define the directory where your templates are stored
template_dir = '.'

# Initialize Jinja2 environment
env = Environment(loader=FileSystemLoader(template_dir))

# Load the template
template = env.get_template('cisco_command_runner_tasks_jinja_template.j2')

# Define your show commands
commands = [
    'show version',
    'show ip interface brief'
]

# Render the template with the commands
rendered_tasks = template.render(commands=commands)

# Path to the output tasks file
tasks_file_path = 'cisco_tasks.yml'

# Write the rendered tasks to the file
with open(tasks_file_path, 'w') as tasks_file:
    tasks_file.write(rendered_tasks)

print(f"Tasks file '{tasks_file_path}' has been generated.")

# Define the playbook file to append plays
playbook_file_path = 'playbook_tasks.yml'

# Content to append in the playbook file
playbook_content = f"""
- name: Execute Cisco device commands and save outputs
  hosts: cisco_devices
  gather_facts: no
  tasks:
    - import_tasks: cisco_tasks.yml
"""

# Append to or create the playbook file
with open(playbook_file_path, 'a') as playbook_file:
    playbook_file.write(playbook_content)

print(f"Playbook content has been appended to '{playbook_file_path}'.")
