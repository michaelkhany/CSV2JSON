"""
CSV to JSON Converter with Subfolder Check

This script allows the user to convert CSV files to JSON format. The user may provide 
the folder path as a command-line argument when running the script. If not provided, 
the script will request it during runtime. Additionally, the script asks the user if it 
should check subfolders for CSV files to convert them as well.

Usage:
    python script_name.py [folder_name]

    - [folder_name]: (Optional) Path to the folder containing CSV files. If not 
                     provided, the script will prompt for it.

Workflow:
    1. Retrieve folder name from command-line argument or user input.
    2. Ask the user if subfolders should be checked for CSV files.
    3. Find and list all CSV files in the specified folder (and subfolders if chosen).
    4. Convert each CSV file to a JSON file, saving it with the same name and directory
       path as the original CSV, and display a progress bar during the process.
"""

import importlib.util
import subprocess
import sys
import os

def check_and_install(package_name):
    """
    Check if a Python package is installed. If not, install it.

    Args:
    - package_name (str): The name of the package to check/install.

    Returns:
    None
    """
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        print(f"{package_name} not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
    else:
        print(f"{package_name} is already installed.")

# Check and install necessary packages
check_and_install("tqdm")

# Now, import the installed package
from tqdm import tqdm
import csv
import json

def convert_csv_to_json(csv_path, json_path):
    with open(csv_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        data_list = list(csv_reader)

    with open(json_path, mode='w', encoding='utf-8') as file:
        json.dump(data_list, file, ensure_ascii=False, indent=4)

# Check if a folder name is provided as a command-line argument
if len(sys.argv) > 1:
    folder_name = sys.argv[1]
    check_subfolders ="y"
else:
    folder_name = "datasets"
    print(" Directory 'datasets' selected automatically.")
    # Ask the user if subfolders should be checked
    check_subfolders = input("Do you want to check subfolders too? (y/n): ").strip().lower()

csv_files = []

# Get all csv files in the specified folder (and optionally subfolders)
if check_subfolders == 'y':
    for root, dirs, files in os.walk(folder_name):
        csv_files.extend([os.path.join(root, file) for file in files if file.endswith('.csv')])
else:
    csv_files = [os.path.join(folder_name, f) for f in os.listdir(folder_name) if f.endswith('.csv')]

# Iterate through each file and convert them to JSON
for csv_file_path in tqdm(csv_files, desc='Converting CSV to JSON', unit='file'):
    json_file_path = os.path.splitext(csv_file_path)[0] + '.json'
    convert_csv_to_json(csv_file_path, json_file_path)
