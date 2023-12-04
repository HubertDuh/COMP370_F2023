import pandas as pd

format_str = '%m/%d/%Y %H:%M:%S %p'

incidents = pd.read_csv('nyc_2020_incidents_with_headers.csv')
incidents = incidents.dropna(subset=['Incident Zip']).copy()
incidents = incidents.dropna(subset=['Closed Date'])
incidents['Created Date'] = pd.to_datetime(incidents['Created Date'], format=format_str, errors='coerce')
incidents['Closed Date'] = pd.to_datetime(incidents['Closed Date'], format=format_str, errors='coerce')
incidents = incidents[incidents['Created Date'] <= incidents['Closed Date']]

closed_incidents = incidents[incidents['Status'] == 'Closed'].copy()

closed_incidents['Response Time'] = (closed_incidents['Closed Date'] - closed_incidents[
    'Created Date']).dt.total_seconds() / 3600  # in hours

grouped_data = closed_incidents.groupby(
    ['Incident Zip', closed_incidents['Closed Date'].dt.month])['Response Time'].mean().reset_index()
grouped_data.rename(columns={'Incident Zip': 'Zipcode', 'Closed Date': 'Month',
                             'Response Time': 'Avg Response Time (hours)'}, inplace=True)

grouped_data.to_csv('preprocessed_data.csv', index=False)
