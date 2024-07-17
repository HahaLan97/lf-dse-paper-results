import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# Function to process a single CSV file
def process_csv(file_path):
    df = pd.read_csv(file_path)
    return df.iloc[:, 0].tolist(), df.iloc[:, 1].tolist()  # Return the first and second columns as lists

# List of folders containing CSV files
folders = ['mocasin', 'linux', 'linux-ondemand', 'linux-schedutil', 'linux-powersaver']

# Dictionary to store data for each configuration
data_exec_time = {folder: [] for folder in folders}
data_total_energy = {folder: [] for folder in folders}

# Read data from CSV files
for folder in folders:
    for file in os.listdir(folder):
        if file.endswith('.csv'):
            file_path = os.path.join(folder, file)
            exec_time, total_energy = process_csv(file_path)
            data_exec_time[folder].extend(exec_time)
            data_total_energy[folder].extend(total_energy)

# Calculate statistics for execution time
averages_exec_time = [np.mean(data_exec_time[folder]) for folder in folders]
mins_exec_time = [np.min(data_exec_time[folder]) for folder in folders]
maxs_exec_time = [np.max(data_exec_time[folder]) for folder in folders]

# Calculate statistics for total energy
averages_total_energy = [np.mean(data_total_energy[folder]) for folder in folders]
mins_total_energy = [np.min(data_total_energy[folder]) for folder in folders]
maxs_total_energy = [np.max(data_total_energy[folder]) for folder in folders]

# Create the bar plot
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot bars for averages of execution time
bar_width = 0.35
index = np.arange(len(folders))
bars_exec_time = ax1.bar(index, averages_exec_time, bar_width, color='#83c5be', label='Average Execution Time')

# Add error bars for min and max of execution time
ax1.errorbar(index, averages_exec_time, yerr=[np.array(averages_exec_time) - np.array(mins_exec_time), np.array(maxs_exec_time) - np.array(averages_exec_time)], 
             fmt='none', color='black', capsize=5)

# Customize the first y-axis
ax1.set_xlabel('Configurations')
ax1.set_ylabel('Execution Time (s)')
ax1.set_ylim(12, 17)
ax1.set_title('Execution Time and Total Energy')

# Adding the label for the 5th bar (linux-powersaver) at the upper limit of y-axis
fifth_bar_height_exec = averages_exec_time[4]
ax1.text(index[4], 17,
         f'{fifth_bar_height_exec:.2f}', ha='center', va='bottom', color='black')

# Create a second y-axis for total energy
ax2 = ax1.twinx()
bars_total_energy = ax2.bar(index + bar_width, averages_total_energy, bar_width, color='#ffadad', label='Average Total Energy')

# Add error bars for min and max of total energy
ax2.errorbar(index + bar_width, averages_total_energy, yerr=[np.array(averages_total_energy) - np.array(mins_total_energy), np.array(maxs_total_energy) - np.array(averages_total_energy)], 
             fmt='none', color='black', capsize=5)

# Customize the second y-axis
ax2.set_ylabel('Total Energy (J)')
ax2.set_ylim(80, 130)

# Adding the label for the 5th bar (linux-powersaver) at the upper limit of y-axis for total energy
fifth_bar_height_energy = averages_total_energy[4]
ax2.text(index[4] + bar_width, 130,
         f'{fifth_bar_height_energy:.2f}', ha='center', va='bottom', color='black')

# Rotate x-axis labels if they're too long
plt.xticks(index + bar_width / 2, folders, rotation=45, ha='right')

# Adding legends
fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9), bbox_transform=ax1.transAxes)

plt.tight_layout()

# Save the plot as an SVG file
plt.savefig("time_vs_energy.svg", format='svg', bbox_inches='tight')
# plt.show()
