from bokeh.io import curdoc
from bokeh.plotting import figure, show
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Select, Legend
import pandas as pd

# Load your data from zip_total_avg.csv
data = pd.read_csv("zip_total_avg.csv")

# Assuming your data columns are named "Total", "11234", "11210", etc.
zipcodes = data.columns[1:]  # Extract zip code column names

# Convert zipcodes to a list of tuples for Select options
zipcodes_options = [(zip, zip) for zip in zipcodes]

# Create Bokeh widgets
zipcode_select_1 = Select(title="Select Zipcode 1", options=zipcodes_options, value=zipcodes[0])
zipcode_select_2 = Select(title="Select Zipcode 2", options=zipcodes_options, value=zipcodes[1])

# Create a Bokeh plot
plot = figure(title="Monthly Average Response Time",
              x_axis_label="Month",
              y_axis_label="Response Time (hours)")

# Define data sources
source_total = ColumnDataSource(data={"x": data.index, "y": data["Total"]})
source_zipcode_1 = ColumnDataSource(data={"x": data.index, "y": data[zipcode_select_1.value]})
source_zipcode_2 = ColumnDataSource(data={"x": data.index, "y": data[zipcode_select_2.value]})

# Create line glyphs for the plot
line_total = plot.line("x", "y", source=source_total, line_width=2, line_color="blue", legend_label="Total")
line_zipcode_1 = plot.line("x", "y", source=source_zipcode_1, line_width=2, line_color="green", legend_label=zipcode_select_1.value)
line_zipcode_2 = plot.line("x", "y", source=source_zipcode_2, line_width=2, line_color="red", legend_label=zipcode_select_2.value)

# Add a legend to the plot
legend = Legend(items=[("Total", [line_total]), (zipcode_select_1.value, [line_zipcode_1]), (zipcode_select_2.value, [line_zipcode_2])])
plot.add_layout(legend)

# Define a callback function to update the plot when dropdowns change
def update_plot(attr, old_value, new_value):
    selected_zipcode_1 = zipcode_select_1.value
    selected_zipcode_2 = zipcode_select_2.value

    # Update data sources based on selected zip codes
    source_zipcode_1.data = {"x": data.index, "y": data[selected_zipcode_1]}
    source_zipcode_2.data = {"x": data.index, "y": data[selected_zipcode_2]}

    # Update legend
    legend.items = [("Total", [line_total]), (zipcode_select_1.value, [line_zipcode_1]), (zipcode_select_2.value, [line_zipcode_2])]

zipcode_select_1.on_change("value", update_plot)
zipcode_select_2.on_change("value", update_plot)

# Create a layout for the dashboard
layout = column(zipcode_select_1, zipcode_select_2, plot)

# Add the layout to the current document
curdoc().add_root(layout)

# Display the Bokeh dashboard
show(layout)
