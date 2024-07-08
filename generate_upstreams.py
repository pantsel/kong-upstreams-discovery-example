import json
import yaml
import argparse

def generate_upstreams_json(records_file, key, output_file):
    with open(records_file, 'r') as f:
        records = json.load(f)

    upstreams = []
    if key in records:
        for record in records[key]:
            upstreams.append({
                'name': record['upstream_name'],
                'targets': [
                    {'target': record['upstream_url']}
                ]
            })

    output_data = {'upstreams': upstreams}

    with open(output_file, 'w') as f:
        yaml.dump(output_data, f, default_flow_style=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate upstreams.yaml from records.json.')
    parser.add_argument('--records-file', '-r', required=True, help='Path to the records.json file.')
    parser.add_argument('--key', '-k', required=True, help='Key to look for in the records.json file.')
    parser.add_argument('--output-file', '-o', required=True, help='Path to the output upstreams.yaml file.')

    args = parser.parse_args()

    generate_upstreams_json(args.records_file, args.key, args.output_file)
