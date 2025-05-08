import os
import json
import math
from pathlib import Path
import argparse


def calculate_geometric_mean(values):
    """Calculate the geometric mean of a list of numerical values."""
    if not values:
        return None
    product = 1.0
    n = len(values)
    for value in values:
        product *= value
    return math.pow(product, 1 / n)


def process_json_files(input_dir, output_file):
    """Process all JSON files in the input directory and generate a summary report."""
    results = []
    ratio_values = []  # Store all ratio values for geometric mean calculation

    # Iterate through all JSON files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(input_dir, filename)

            try:
                with open(filepath, "r") as f:
                    data = json.load(f)

                    # Verify the data is a list
                    if not isinstance(data, list):
                        print(
                            f"Warning: {filename} is not a valid JSON array, skipping"
                        )
                        continue

                    # Find Linux and Asterinas results
                    linux_data = None
                    aster_data = None

                    for item in data:
                        if not isinstance(item, dict):
                            continue

                        if item.get("extra") == "linux_result":
                            linux_data = item
                        elif item.get("extra") == "aster_result":
                            aster_data = item

                    # Validate we have both data points
                    if not linux_data or not aster_data:
                        print(f"Warning: {filename} is missing required data, skipping")
                        continue

                    # Verify units match
                    if linux_data.get("unit") != aster_data.get("unit"):
                        print(f"Warning: {filename} has mismatched units, skipping")
                        continue

                    unit = linux_data["unit"]

                    # Calculate the ratio
                    try:
                        linux_value = float(linux_data["value"])
                        aster_value = float(aster_data["value"])

                        if unit == "µs" or unit == "second":
                            ratio = linux_value / aster_value
                        elif unit == "MB/s" or unit == "MB/sec" or unit == "request per second" or unit =="Requests per second":
                            ratio = aster_value / linux_value
                        else:
                            print(
                                f"Warning: {filename} contains unknown unit: {unit}, skipping"
                            )
                            continue

                        # Format ratio to 3 decimal places
                        ratio_str = f"{ratio:.3f}"
                        ratio_values.append(ratio)  # Store the numerical value

                        results.append(
                            {"file": filename, "unit": unit, "ratio": ratio_str}
                        )

                    except (ValueError, KeyError) as e:
                        print(
                            f"Warning: {filename} contains invalid numeric value or missing field: {e}, skipping"
                        )
                        continue

            except json.JSONDecodeError:
                print(f"Error: {filename} is not a valid JSON file, skipping")
                continue

    # Write the output file
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    # Calculate and print geometric mean if we have ratios
    if ratio_values:
        geo_mean = calculate_geometric_mean(ratio_values)
        print(f"\nGeometric mean of all ratios: {geo_mean:.4f}")
    else:
        print("\nNo valid ratios found to calculate geometric mean")

    print(f"\nProcessing complete. Results saved to {output_file}")


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Process JSON benchmark files and calculate performance ratios."
    )
    parser.add_argument(
        "input_directory", help="Directory containing JSON files to process"
    )
    parser.add_argument("output_filename", help="Filename for the output JSON results")

    args = parser.parse_args()

    input_directory = args.input_directory
    output_filename = args.output_filename

    # Validate input directory exists
    if not os.path.isdir(input_directory):
        print(f"Error: Directory {input_directory} does not exist")
        exit(1)

    process_json_files(input_directory, output_filename)
