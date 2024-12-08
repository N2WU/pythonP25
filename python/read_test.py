import yaml

with open('config.yml', 'r') as f:
       yaml_data = yaml.load(f, Loader=yaml.SafeLoader)

print(yaml_data)
print(yaml_data['mac'])