import yaml
from yaml import SafeLoader

with open('config.yml', 'r') as f:
    data = yaml.full_load(f)

# Print the values as a dictionary
with open('config.yml', 'r') as f:
    yaml_data = list(yaml.load_all(f, Loader=SafeLoader))
    print(yaml_data)
