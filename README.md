# Network Automation Scripts
Posting up some generic network automation scripts to give people a good starting point 

Scripts will mainly be python, powershell and ansible playbooks/tasks. 

## Scripts
Will create a readthedocs for it but mainly:
### Ansible
Scripts to run commands and configs against cisco devices as well as examples and jinja templates and generators for STIG compliance
For Stigs there are two flavors, once that just runs show commands so that it can be completely safe, then a branch that you'd run in dry run to judge for compliance but could remediate by running normally

### Powershell
These are mainly general tasks someone might need to run like ping sweeps, port checks, checking an API, etc. The API check and cisco command runner have GUIs built around them as well. 

### Python
Need to spruce these up a little but as these are scripts I had laying around for various purposes like chekcing an API w/ a django frontent or pyqt frontend, running commands against cisco devices using netmiko and bootstrapping a lab using a custom telnet lib as the python standard telnet lib was deprciated. 

## To Run:
### Python
```python3 -m [script name]```

### Powershell
```[script name].ps1```

### Ansible
```ansible-playbook -i [path to inventory] [playbook name]```
