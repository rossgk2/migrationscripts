import json
import argparse
import os
import sys
import csv
import jmespath

def save_array_to_csv(arr, filename):
    with open(filename, "w", newline='') as file:
        writer = csv.writer(file)
        for elem in arr:
            writer.writerow([elem])

def main():
    parser = argparse.ArgumentParser(description="Saves the agreement IDs from the JSON output of a call to GET /agreements to a .csv.")
    parser.add_argument("agreement_ids_json", help="Full path to the JSON file.")

    args = parser.parse_args()
    file_path = args.agreement_ids_json

    if not os.path.isfile(file_path):
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    try:
        with open(file_path, "r") as file:
            _json = json.load(file)
            agreement_ids = jmespath.search("userAgreementList[*].id", _json)
            save_array_to_csv(agreement_ids, "./agreement_ids.csv")

    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
