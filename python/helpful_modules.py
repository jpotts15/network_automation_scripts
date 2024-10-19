import json
import yaml
import xml.etree.ElementTree as ET
import ipaddress

def read_json(file_path):
    """
    Reads a JSON file and returns its contents as a Python dictionary.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The contents of the JSON file as a Python dictionary.
    """
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

def read_xml(file_path):
    """
    Reads an XML file and returns its root element.

    Args:
        file_path (str): The path to the XML file.

    Returns:
        Element: The root element of the XML tree.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root

def read_yaml(file_path):
    """
    Reads a YAML file and returns its contents as a Python dictionary.

    Args:
        file_path (str): The path to the YAML file.

    Returns:
        dict: The contents of the YAML file as a Python dictionary.
    """
    with open(file_path, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)
    return data

def json_to_dict(file_path):
    """
    Reads a JSON file and returns its contents as a Python dictionary.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The contents of the JSON file as a Python dictionary.
    """
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

def xml_to_dict(file_path):
    """
    Reads an XML file and converts it to a Python dictionary.

    Args:
        file_path (str): The path to the XML file.

    Returns:
        dict: The XML data represented as a Python dictionary.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    return xml_to_dict_recursive(root)

def xml_to_dict_recursive(element):
    """
    Recursively converts an XML element and its children into a Python dictionary.

    Args:
        element (Element): The XML element to convert.

    Returns:
        dict or str: A dictionary representing the XML element and its children,
                     or a string if the element has no children.
    """
    if len(element) == 0:
        return element.text
    result = {}
    for child in element:
        child_data = xml_to_dict_recursive(child)
        if child.tag in result:
            if isinstance(result[child.tag], list):
                result[child.tag].append(child_data)
            else:
                result[child.tag] = [result[child.tag], child_data]
        else:
            result[child.tag] = child_data
    return result

def yaml_to_dict(file_path):
    """
    Reads a YAML file and returns its contents as a Python dictionary.

    Args:
        file_path (str): The path to the YAML file.

    Returns:
        dict: The contents of the YAML file as a Python dictionary.
    """
    with open(file_path, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)
    return data

def dict_to_json(data, file_path):
    """
    Writes a Python dictionary to a JSON file.

    Args:
        data (dict): The dictionary to write to the JSON file.
        file_path (str): The path where the JSON file will be created.
    """
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=2)

def dict_to_xml(data, file_path):
    """
    Writes a Python dictionary to an XML file.

    Args:
        data (dict): The dictionary to write to the XML file.
        file_path (str): The path where the XML file will be created.
    """
    root = dict_to_xml_recursive(data, ET.Element('root'))
    tree = ET.ElementTree(root)
    tree.write(file_path)

def dict_to_xml_recursive(data, parent):
    """
    Recursively converts a Python dictionary to XML elements and appends them to a parent element.

    Args:
        data (dict or list): The data to convert to XML.
        parent (Element): The parent XML element to append to.

    Returns:
        Element: The parent element with the appended XML data.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            child = ET.SubElement(parent, key)
            dict_to_xml_recursive(value, child)
    elif isinstance(data, list):
        for item in data:
            dict_to_xml_recursive(item, parent)
    else:
        parent.text = str(data)
    return parent

def dict_to_yaml(data, file_path):
    """
    Writes a Python dictionary to a YAML file.

    Args:
        data (dict): The dictionary to write to the YAML file.
        file_path (str): The path where the YAML file will be created.
    """
    with open(file_path, 'w') as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False)

class IPConverter:
    def __init__(self, input_file="ip_to_binary_input.json"):
        self.input_file = input_file

    def parse_ip_input(self,input_str):
        try:
            ip_network = ipaddress.ip_network(input_str, strict=False)
            if ip_network.version == 4:
                if '/' in input_str:
                    ip = input_str.split("/")
                    ip = ip[0]
                    subnet = ip[1]
                    return ip, subnet
                elif input_str.count('.') > 4:
                    return "IPv4 in IP+subnet notation"
                else:
                    return "IPv4 address"
            elif ip_network.version == 6:
                if '/' in input_str:
                    return "IPv6 in CIDR notation"
                elif '-' in input_str:
                    return "IPv6 in IP+subnet notation"
                else:
                    return "IPv6 address"
        except ValueError:
            return "Invalid IP address or format"

    def ipv4_to_dec(self,ip):
        # counting and inefficent version
        #ip = '192.168.1.0'
        if "/" in ip:
            ip = ip.split("/")
            ip = ip[0]
            subnet = ip[1]
        ip_list = ip.split(".")
        binary = ""
        octet_counter = ""
        binary_ip = ""
        for octet in ip_list:
            octet = int(octet)
            if octet > 255:
                return "error"
            if octet >= 128:
                octet -= 128
                binary_ip += "1"
            else:
                binary_ip += "0"
            if octet >= 64:
                octet -= 64
                binary_ip += "1"
            else:
                binary_ip += "0"
            if octet >= 32:
                octet -= 32
                binary_ip += "1"
            else:
                binary_ip += "0"
            if octet >= 16:
                octet -= 26
                binary_ip += "1"
            else:
                binary_ip += "0"
            if octet >= 8:
                octet -= 8
                binary_ip += "1"
            else:
                binary_ip += "0"
            if octet >= 4:
                octet -= 4
                binary_ip += "1"
            else:
                binary_ip += "0"
            if octet >= 2:
                octet -= 2
                binary_ip += "1"
            else:
                binary_ip += "0"
            if octet >= 1:
                octet -= 1
                binary_ip += "1 "
            else:
                binary_ip += "0 "

        return binary_ip[0:-1]

    def ip_dec_to_bin(self):
        # input_selector = input("Would you like to change the input json?: (y/n)")
        input_selector = 'n'
        if input_selector.lower()[0] == 'y':
            # Do something with self.input_file here
            #self.input_file = input("Enter file path: ")
            pass

        with open(self.input_file, 'r') as file:
            ip_data = json.load(file)

        print(ip_data)
        return ip_data
    
def dictionary_walker(dict_in, return_dict=None, current_key_path=None, list_limit=None):
    '''
    Walks a dictionary or a list of dictionaries to create a schema/blank dict.
    Handles nested dictionaries and lists of dictionaries.
    Allows limiting the iteration of lists based on a given list length limit.
    '''
    if return_dict is None:
        return_dict = {}
    if current_key_path is None:
        current_key_path = []

    assert isinstance(dict_in, (dict, list)), "Input must be a dictionary or a list"

    if isinstance(dict_in, dict):
        for key, value in dict_in.items():
            # Update the current path with the new key
            new_key_path = current_key_path + [key]

            # Create a reference to the current position in the return_dict
            current_dict = return_dict
            for path_key in current_key_path:
                current_dict = current_dict.setdefault(path_key, {})

            if isinstance(value, dict):
                # If the value is a dictionary, add an empty dict and recurse
                current_dict[key] = {}
                dictionary_walker(value, return_dict, new_key_path, list_limit)
            
            elif isinstance(value, list):
                # If the value is a list, check its length against the list_limit
                if list_limit is not None and len(value) == list_limit:
                    continue  # Skip adding this list if it meets the list_limit criteria
                
                current_dict[key] = []
                for item in value:
                    if isinstance(item, dict):
                        # If the list contains a dict, create a template for it
                        list_item_template = {}
                        current_dict[key].append(list_item_template)
                        dictionary_walker(item, list_item_template, [], list_limit)
                    else:
                        # Otherwise, just append a placeholder
                        current_dict[key].append(None)
            
            else:
                # If it's not a dict or list, add an empty value or None
                current_dict[key] = None

    elif isinstance(dict_in, list):
        return_dict = []
        if list_limit is not None and len(dict_in) == list_limit:
            return return_dict  # Skip processing this list if it meets the list_limit criteria

        for item in dict_in:
            if isinstance(item, dict):
                # If the list contains a dict, process it
                list_item_template = {}
                return_dict.append(list_item_template)
                dictionary_walker(item, list_item_template, [], list_limit)
            else:
                # Otherwise, just append a placeholder
                return_dict.append(None)

    return return_dict