import json
import yaml
import argparse

def generate_yaml(records_file, key, output_file):
    with open(records_file, 'r') as f:
        records = json.load(f)

    rules = []
    if key in records:
        for record in records[key]:
            rules.append({
                'upstream_name': record['upstream_name'],
                'condition': {
                    'location': record['location']
                }
            })

    output_data = {
        '_format_version': '3.0',
        'add-plugins': [
            {
                'selectors': [
                    "$..services[0]"
                ],
                'overwrite': False,
                'plugins': [
                    {
                        'name': 'route-by-header',
                        'config': {
                            'rules': rules
                        },
                        'enabled': True
                    }
                ]
            }
        ]
    }

    with open(output_file, 'w') as f:
        yaml.dump(output_data, f, default_flow_style=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a YAML file from records.json.')
    parser.add_argument('--records-file', '-r', required=True, help='Path to the records.json file.')
    parser.add_argument('--key', '-k', required=True, help='Key to look for in the records.json file.')
    parser.add_argument('--output-file', '-o', required=True, help='Path to the output YAML file.')

    args = parser.parse_args()

    generate_yaml(args.records_file, args.key, args.output_file)
