from bokeh.models import ColumnDataSource, Select, FactorRange
from bokeh.plotting import curdoc, figure, show
from bokeh.layouts import column
import pandas as pd

month_range = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September']


def month_sort(x):
    return month_range.index(x)


# Load pre-processed data (monthly averages for each zipcode)
# Replace 'preprocessed_data.csv' with the actual file path
df = pd.read_csv('preprocessed_data.csv')
df['Month'] = pd.to_datetime(df['Month'], format='%m').dt.strftime('%B')
df['Month'] = df['Month'].sort_values()


df_year_round = df.groupby('Month')['Avg Response Time (hours)'].mean().reset_index(name='Average Response Time')
df_year_round = df_year_round.sort_values(by=['Month'], key=lambda x: x.map(month_sort))
source_year_round = ColumnDataSource(df_year_round)

plot = figure(x_range=month_range, height=600, width=1000, title='Monthly Average Response Time',
              toolbar_location=None, tools="", x_axis_label="Month", y_axis_label="Avg Response Time (hours)")


zipcodes = [str(zipcode) for zipcode in df['Zipcode'].unique()]

base_value = df.at[0, 'Zipcode']

# Create dropdown widgets for selecting zipcodes
zipcode1_select = Select(title="Select Zipcode 1", options=zipcodes, value='83.0')
zipcode2_select = Select(title="Select Zipcode 2", options=zipcodes, value='83.0')

zipcode1 = float(zipcode1_select.value)
zipcode2 = float(zipcode2_select.value)

df_zipcode1 = df[df['Zipcode'] == zipcode1]
df_zipcode1 = df_zipcode1.sort_values(by=['Month'], key=lambda x: x.map(month_sort))
source_zipcode1 = ColumnDataSource(df_zipcode1)

df_zipcode2 = df[df['Zipcode'] == zipcode2]
df_zipcode2 = df_zipcode2.sort_values(by=['Month'], key=lambda x: x.map(month_sort))
source_zipcode2 = ColumnDataSource(df_zipcode2)

# Create a line plot

# Add lines for the three curves
year_average = plot.line(x='Month', y='Average Response Time', source=source_year_round, line_color='blue',
                         legend_label='All 2020')
zipcode1_average = plot.line(x='Month', y='Avg Response Time (hours)', source=source_zipcode1, line_color='green',
                             legend_label='Zipcode 1')
zipcode2_average = plot.line(x='Month', y='Avg Response Time (hours)', source=source_zipcode2, line_color='red',
                             legend_label='Zipcode 2')

# Add a legend
plot.legend.title = 'Curves'


# Define a callback function to update the plot
def update_plot(attrname, old_value, new_value):
    selected_zipcode1 = float(zipcode1_select.value)
    selected_zipcode2 = float(zipcode2_select.value)
    # Update the data source with the selected zipcodes
    new_zip1 = df[df['Zipcode'] == selected_zipcode1].sort_values(by=['Month'], key=lambda x: x.map(month_sort))
    new_zip2 = df[df['Zipcode'] == selected_zipcode2].sort_values(by=['Month'], key=lambda x: x.map(month_sort))

    zip1 = ColumnDataSource(new_zip1)
    zip2 = ColumnDataSource(new_zip2)

    zipcode1_average.data_source.data = dict(zip1.data)
    zipcode2_average.data_source.data = dict(zip2.data)


# Add callback to update the plot when zipcodes are changed
zipcode1_select.on_change('value', update_plot)
zipcode2_select.on_change('value', update_plot)

# Create layout for the dashboard
layout = column(zipcode1_select, zipcode2_select, plot)

# Add layout to the current document
curdoc().add_root(layout)
