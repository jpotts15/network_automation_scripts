from jinja2 import Environment, FileSystemLoader
import os

# Define the variables for rendering
variables = {
    'stig_id': 'V-215832',
    'check_command': 'service password-encryption',
    'pass_condition': 'config_output.diff | length > 1',
    'task_file_name': 'example_stig_task_v215832.yml'
}

# Set up the Jinja2 environment and load the template
env = Environment(loader=FileSystemLoader('templates'))

# Render the task file
task_template = env.get_template('example_stig_task_jinja_template_ios_config.j2')
rendered_task = task_template.render(variables)
task_file_path = f"./{variables['task_file_name']}"

# Write the rendered task file to disk
with open(task_file_path, 'w') as f:
    f.write(rendered_task)

# Prepare the playbook import statement
playbook_import_statement = f"- name: STIG {variables['stig_id']}\n  import_tasks: ./{variables['task_file_name']}"

# Append to playbook_tasks.yml
playbook_tasks_file = 'playbook_tasks.yml'

# Check if the file exists
if os.path.exists(playbook_tasks_file):
    # Append to the existing file
    with open(playbook_tasks_file, 'a') as f:
        f.write(f"\n{playbook_import_statement}\n")
else:
    # Create the file and write the import statement
    with open(playbook_tasks_file, 'w') as f:
        f.write(f"{playbook_import_statement}\n")

print(f"Task file generated: {task_file_path}")
print(f"Playbook import statement appended to: {playbook_tasks_file}")
