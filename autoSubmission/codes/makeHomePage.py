import argparse
import os
import json
from datetime import datetime

import re
import json

def read_or_initialize_log(path):
    if os.path.exists(path):
        with open(path, 'r') as file:
            content = file.read()
            # Remove the JS variable assignment part
            json_content = content.replace('const trainingLogs = ', '').rstrip(';')
            # Use a regular expression to add double quotes around the keys
            json_content = re.sub(r'([{,]\s*)(\w+)(\s*:)', r'\1"\2"\3', json_content)
            return json.loads(json_content)
    return {}


def write_log(path, log_data):
    with open(path, 'w') as file:
        file.write(f'const trainingLogs = {json.dumps(log_data, indent=2)};')

def update_log(args, log_data):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    # Conditionally format detail based on the status
    if args.status == "Training" and args.epoch is not None and args.maxEpoch is not None:
        detail = {"epoch": args.epoch, "maxEpoch": args.maxEpoch}
    elif args.status == "Plotting" and args.plot is not None:
        detail = args.plot
    else:
        detail = "Status detail not specified"

    new_entry = {
        'status': args.status,
        'detail': detail,
        'updatedDate': now
    }
    
    # Create a new dictionary for the updated log data
    updated_log_data = {}
    
    # Check if the trainingName already exists and update or add it accordingly
    if args.trainingName in log_data:
        existing_entries = log_data[args.trainingName]
        existing_entries.append(new_entry)
        updated_log_data[args.trainingName] = existing_entries
    else:
        updated_log_data[args.trainingName] = [new_entry]
    
    # Update the new log data dictionary with the existing log data, ensuring new entry stays on top
    for key, value in log_data.items():
        if key not in updated_log_data:
            updated_log_data[key] = value

    return updated_log_data



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update or create training status HTML file with advanced features.')
    parser.add_argument('--trainingName', help='Unique name of the training session')
    parser.add_argument('--status', help='Current status of the training')
    parser.add_argument('--plot', help='Plot text for Plotting status, optional')
    parser.add_argument('--epoch', type=int, help='Current epoch, only for Training status')
    parser.add_argument('--maxEpoch', type=int, help='Maximum number of epochs, only for Training status')
    parser.add_argument('--reset', action='store_true', help='Reset the table, removing all entries')

    args = parser.parse_args()

    # Determine the path to log.js
    script_path = os.path.realpath(__file__)
    index_path = os.path.dirname(script_path)
    log_path = os.path.join(index_path, 'log.js')

    # Read or initialize log data
    log_data = {} if args.reset else read_or_initialize_log(log_path)
    
    if not args.reset:
        log_data = update_log(args, log_data)


    # Write the updated or new log data to log.js
    write_log(log_path, log_data)
