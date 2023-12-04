import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Assuming the date format in your dataset is '%m/%d/%Y %I:%M:%S %p'
format_str = '%m/%d/%Y %I:%M:%S %p'

# Load the dataset
df = pd.read_csv('~/Documents/PycharmProjects/COMP370_HW04/nyc_2020_incidents_with_headers.csv')

# Convert 'Created Date' and 'Closed Date' to datetime format
df['Created Date'] = pd.to_datetime(df['Created Date'], format=format_str, errors='coerce')
df['Closed Date'] = pd.to_datetime(df['Closed Date'], format=format_str, errors='coerce')

rodent_df = df[df['Complaint Type'].str.contains('Rodent', case=False, na=False)]

structure_types = rodent_df['Location Type'].unique()

structure_counts = rodent_df['Location Type'].value_counts()

# Plot the results
plt.figure(figsize=(12, 6))
structure_counts.plot(kind='bar', color='skyblue')
plt.xlabel('Structure Types')
plt.ylabel('Number of Complaints')
plt.title('Types of Structures Where Rodents Create Sanitation Issues')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('task2_plot.jpg')
plt.show()