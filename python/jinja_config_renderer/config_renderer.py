from jinja2 import Environment, FileSystemLoader


def render_config(device_data, template_name):
    # Set up Jinja2 environment to load templates from current directory
    env = Environment(loader=FileSystemLoader('.'))

    # Load and render the template
    template = env.get_template(template_name)
    config = template.render(device_data)

    return config


if __name__ == "__main__":
    # Example dictionary to input data
    device_data_static = {
        'hostname': 'Device1'
    }

    device_data_interface = {
        'hostname': 'Device1',  # even though this is common, we might want it in both templates
        'interface': 'GigabitEthernet0/1',
        'description': 'Uplink to Core',
        'ip': '192.168.1.2',
        'subnet': '255.255.255.0'
    }

    static_config = render_config(device_data_static, "template1.jinja")
    interface_config = render_config(device_data_interface, 'template2.jinja')

    merged_config = static_config + "\n" + interface_config
    print(merged_config)
