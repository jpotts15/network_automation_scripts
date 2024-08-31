#import modules for data structurs, yaml from pyyaml
import json
import yaml
import xml.etree.ElementTree as ET

'''
# This script will be to familiarize with data types covered in devnet. The main structured data formats are xml, json
and yaml. Don't confuse these with the fundamental python data structures like string, list, dict, etc. 

## Data structures and their formats, you could just pop those to a string and then read them but easier to work off a 
external file 

### xml example
<?xml version="1.0" encoding="utf-8"?>
<root>
 <countries>
  <element>
   <hemisphere>Northern</hemisphere>
   <name>USA</name>
    </element>
    <element>
    <hemisphere>Northern</hemisphere>
    <name>Germany</name>
   </element>
   <element>
    <hemisphere>Southern</hemisphere>
    <name>Australia</name>
   </element>
  </countries>
</root>

### json example
{
  "countries": [
    {
      "name": "USA",
      "hemisphere": "northern"
    },

    {
      "name": "Germany",
      "hemisphere": "northern"
    },

    {
      "name": "Australia",
      "hemisphere": "southern"
    }
  ]
}

### yaml example
countries:
  - name: 'USA'
    hemisphere: 'northern'
  - name: 'Germany'
    hemisphere: 'northern'
  - name: 'Australia'
    hemisphere: 'southern'
    
in script will just call files directly 
'''

# Modules to do work

def read_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

def read_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root

def read_yaml(file_path):
    with open(file_path, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)
    return data

def json_to_dict(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

def xml_to_dict(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return xml_to_dict_recursive(root)

def xml_to_dict_recursive(element):
    if len(element) == 0:
        return element.text
    result = {}
    for child in element:
        child_data = xml_to_dict_recursive(child)
        if child.tag in result:
            if type(result[child.tag]) is list:
                result[child.tag].append(child_data)
            else:
                result[child.tag] = [result[child.tag], child_data]
        else:
            result[child.tag] = child_data
    return result

def yaml_to_dict(file_path):
    with open(file_path, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)
    return data

def dict_to_json(data, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=2)

def dict_to_xml(data, file_path):
    root = dict_to_xml_recursive(data, ET.Element('root'))
    tree = ET.ElementTree(root)
    tree.write(file_path)

def dict_to_xml_recursive(data, parent):
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
    with open(file_path, 'w') as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False)

# set files to variables for ease
json_file_path = '../structured_data_examples/json_example.json'
xml_file_path = '../structured_data_examples/xml_example.xml'
yaml_file_path = '../structured_data_examples/yaml_example.yaml'

json_output_path = '../structured_data_examples/json_output_example.json'
xml_output_path = '../structured_data_examples/xml_output_example.xml'
yaml_output_path = '../structured_data_examples/yaml_output_example.yaml'

# setup the basic dictionary to convert back to other formats
data = {'countries': [{'name': 'USA', 'hemisphere': 'northern'}, {'name': 'Germany', 'hemisphere': 'northern'}, {'name': 'Australia', 'hemisphere': 'southern'}]}

# xml usage

# Convert JSON file to dictionary
json_data = json_to_dict(json_file_path)
print("JSON Data as Dictionary:")
print(json_data)
print("\n")

# Convert XML file to dictionary
xml_data = xml_to_dict(xml_file_path)
print("XML Data as Dictionary:")
print(xml_data)
print("\n")

# Convert YAML file to dictionary
yaml_data = yaml_to_dict(yaml_file_path)
print("YAML Data as Dictionary:")
print(yaml_data)

# Convert and save to JSON file
dict_to_json(data, json_output_path)
print(f"Data saved to {json_output_path}")

# Convert and save to XML file
dict_to_xml(data, xml_output_path)
print(f"Data saved to {xml_output_path}")

# Convert and save to YAML file
dict_to_yaml(data, yaml_output_path)
print(f"Data saved to {yaml_output_path}")