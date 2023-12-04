import sys
import pandas as pd
import argparse

# awk -F',' '$2 ~ /2020/' nyc_311_limit.csv > nyc_2020_incidents.csv

# echo "Unique Key,Created Date,Closed Date,Agency,Agency Name,Complaint Type,Descriptor,Location Type,Incident Zip,
# Incident Address,Street Name,Cross Street 1,Cross Street 2,Intersection Street 1,Intersection Street 2,Address Type,
# City,Landmark,Facility Type,Status,Due Date,Resolution Description,Resolution Action Updated Date,Community Board,BBL,
# Borough,X Coordinate (State Plane),Y Coordinate (State Plane),Open Data Channel Type,Park Facility Name,Park Borough,
# Vehicle Type,Taxi Company Borough,Taxi Pick Up Location,Bridge Highway Name,Bridge Highway Direction,Road Ramp,
# Bridge Highway Segment,Latitude,Longitude,Location" > headers.csv

# cat headers.csv nyc_2020_incidents.csv > nyc_2020_incidents_with_headers.csv

format_str = '%m/%d/%Y %H:%M:%S %p'


# def filter_df(df):
#     df = df.dropna(subset=['Incident Zip']).copy()
#     df = df.dropna(subset=['Closed Date'])
#
#     df['Created Date'] = pd.to_datetime(df['Created Date'], format=format_str, errors='coerce')
#     df['Closed Date'] = pd.to_datetime(df['Closed Date'], format=format_str, errors='coerce')
#
#     filtered_df = df[df['Created Date'] >= df['Closed Date']]
#     return filtered_df

def filter_by_date_range(df, start_date, end_date):
    return df[(df['Created Date'] >= start_date) & (df['Created Date'] <= end_date)]


def count_complaints_per_borough(df):
    return df.groupby(['Complaint Type', 'Borough']).size().reset_index(name='Count')


def parse_args(args):
    parser = argparse.ArgumentParser(prog='borough_complaints.py',
                                     description='Counts the number of each complaint type per borough for a given '
                                                 '(creation) date range')
    parser.add_argument('-i', '--input', required=True, help='Input CSV file')
    parser.add_argument('-s', '--start-date', required=True, help='Start Date (mm/dd/yyyy)')
    parser.add_argument('-e', '--end-date', required=True, help='End Date (mm/dd/yyyy)')
    parser.add_argument('-o', '--output', help='Output file (optional)')

    return parser.parse_args(args)


def main():
    args = parse_args(sys.argv[1:])


    try:
        df = pd.read_csv(args.input)
    except FileNotFoundError:
        print(f"FileNotFoundError: File '{args.input}' not found.")
        return

    filtered_df = filter_by_date_range(df, args.start_date, args.end_date)
    result_df = count_complaints_per_borough(filtered_df)

    if args.output:
        result_df.to_csv(args.output, index=False)
        sys.stdout.write(args.output)
    else:
        print(result_df.to_csv(index=False))


if __name__ == '__main__':
    main()
