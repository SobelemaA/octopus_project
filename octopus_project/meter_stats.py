import argparse
import datetime
import sys
from pathlib import Path

# Define parser and arguments
def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("path", default='meter_readings', help="file path for flow")
    parser.add_argument("-c", "--count", action="store_true", help="count of meters")
    parser.add_argument("-sv", "--sum_valid", action="store_true", help="total sum of valid meter readings")
    parser.add_argument("-si", "--sum_invalid", action="store_true", help="total sum of invalid meter readings")
    parser.add_argument("-hv", "--highest_valid", action="store_true", help="highest valid meter reading")
    parser.add_argument("-lv", "--lowest_valid", action="store_true", help="lowest valid meter reading")
    parser.add_argument("-nr", "--newest_reading", action="store_true", help="most recent meter reading")
    parser.add_argument("-or", "--oldest_reading", action="store_true", help="oldest meter reading")
    return parser.parse_args(args)

def open_meter_readings_file(target_dir: str) -> [str]:
    with open(target_dir, 'r') as file:
        lines = file.readlines()

    file.close()

    return lines

# Dictionary to store values from flow
def create_dictionary() -> dict:
    meter_values = {
        "meter_id": [],
        "reading_id": [],
        "value": [],
        "date": [],
        "status": []
    }
    return meter_values

# Parse file to dictionary, converting corresponding values to appropriate datatypes
def parse_file_to_dict(meter_values: dict, lines: [str]):
    i = 1
    while not lines[i].startswith("FOOTER|"):
        split_line = lines[i].split("|")
        # print(split_line)
        if split_line[0] == "METER":
            meter_values['meter_id'].append(split_line[1])
        elif split_line[0] == "READING":
            meter_values['reading_id'].append(split_line[1])
            meter_values['value'].append(float(split_line[2]))
            meter_values['date'].append(datetime.datetime.strptime(split_line[3], "%Y%m%d"))
            meter_values['status'].append(split_line[4])
        i += 1

# Count number of meters
def count_meters(meter_values_meter_id: [float]) -> int:
    return len(meter_values_meter_id)

# Calculate total valid meter readings
def total_valid_meter_readings(meter_values_status: [str]) -> int:
    return meter_values_status.count('V')

# Calculate total invalid meter readings
def total_invalid_meter_readings(meter_values_status: [str]) -> int:
    return meter_values_status.count('F')

# List all valid readings
# Same code can be used for both highest and lowest valid readings
def list_valid_readings(meter_values_value: [float], meter_values_status: [str]) -> [float]:
    list_of_valid_readings = []
    for j in range(len(meter_values_value)):
        if meter_values_status[j] == "V":
            list_of_valid_readings.append(meter_values_value[j])
    return list_of_valid_readings

def main():
    args = parse_args(sys.argv[1:])
    target_dir = Path(args.path)
    lines = open_meter_readings_file(target_dir)
    meter_values = create_dictionary()
    parse_file_to_dict(meter_values, lines)

    if args.count:
        no_of_meters = count_meters(meter_values['meter_id'])
        print(f"Number of meters: {no_of_meters}")

    if args.sum_valid:
        valid_meters = total_valid_meter_readings(meter_values['status'])
        print(f"Total valid meters: {valid_meters}")

    if args.sum_invalid:
        invalid_meters = total_invalid_meter_readings(meter_values['status'])
        print(f"Total invalid meters: {invalid_meters}")

    if args.highest_valid:
        valid_readings = list_valid_readings(meter_values['value'], meter_values['status'])
        print(f"Highest valid meter reading: {max(valid_readings)}")

    if args.lowest_valid:
        valid_readings = list_valid_readings(meter_values['value'], meter_values['status'])
        print(f"Lowest valid meter reading: {min(valid_readings)}")

    if args.newest_reading:
        newest_date = max(meter_values['date'])
        index_max_date = meter_values['date'].index(newest_date)
        print(f"Newest Reading: {newest_date} : {meter_values['value'][index_max_date]}")

    if args.oldest_reading:
        oldest_date = min(meter_values['date'])
        index_min_date = meter_values['date'].index(oldest_date)
        print(f"Oldest Reading: {oldest_date} : {meter_values['value'][index_min_date]}")

