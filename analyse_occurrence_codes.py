
import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the Excel file
modified_data = pd.read_excel("occurrence_data.xlsx")

# Extract the "type" value from the "Occurrence code" column
modified_data['type'] = modified_data['Occurrence code'].str[-2]

# Convert the "Start date" and "Finish date" columns to datetime format
modified_data['Start date'] = pd.to_datetime(modified_data['Start date'], errors='coerce')
modified_data['Finish date'] = pd.to_datetime(modified_data['Finish date'], errors='coerce')

# Find the earliest "Start date" and the latest "Finish date" for each "type"
earliest_start = modified_data.groupby('type')['Start date'].min()
latest_finish = modified_data.groupby('type')['Finish date'].max()

# Plotting the modified timeline with bars for each "type"
plt.figure(figsize=(15, 8))

# Generate bars for each type
for type_value in earliest_start.index:
    plt.barh(type_value,
             left=earliest_start[type_value].year,
             width=latest_finish[type_value].year - earliest_start[type_value].year + 1)

plt.xlabel('Year')
plt.ylabel('Type')
plt.title('Timeline of Earliest "Start Date" to Latest "Finish Date" for Each "Type"')
plt.grid(axis='x')
plt.xticks(rotation=90)  # Rotate x-axis labels vertically
plt.xticks(range(earliest_start.min().year, latest_finish.max().year + 1))  # Show each year value on the x-axis
plt.tight_layout()
plt.show()