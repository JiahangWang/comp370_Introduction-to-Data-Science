#!/usr/bin/env python
import argparse
import pandas as pd
import warnings


warnings.filterwarnings("ignore")

def load_data(input_file):
    try:
        data = pd.read_csv(input_file)
        return data
    except FileNotFoundError:
        print("Input file not found.")
        exit(1)

def filter_data(data, start_date, end_date):
    mask = (data['Created Date'] >= start_date) & (data['Closed Date'] <= end_date)
    return data[mask]

def main():
    parser = argparse.ArgumentParser(description="Count the number of complaint types per borough within a given creation date range.")
    parser.add_argument("-i", "--input", help="Input CSV file", required=True)
    parser.add_argument("-s", "--start_date", help="Start date (YYYY-MM-DD)", required=True)
    parser.add_argument("-e", "--end_date", help="End date (YYYY-MM-DD)", required=True)
    parser.add_argument("-o", "--output", help="Output CSV file (optional)")

    args = parser.parse_args()

    data = load_data(args.input)
    filtered_data = filter_data(data, args.start_date, args.end_date)

    result = filtered_data.groupby(['Complaint Type', 'Borough']).size().reset_index(name='Count')
    result['Count'] = result['Count'].astype(int)  # Convert the 'Count' column data type to integer

    if args.output:
        result.to_csv(args.output, index=False, header=["complaint type", "borough", "count"])
    else:
        print(result.to_csv(index=False, header=["complaint type", "borough", "count"]))

if __name__ == "__main__":
    main()