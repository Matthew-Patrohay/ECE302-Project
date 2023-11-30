import os
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd
import re

def natural_sort_key(s):
    """
    Split the input string into numeric and non-numeric parts and return as a tuple.
    This allows sorting strings in a way that numbers are considered in their numeric value.
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

def count_turns(solution):
    # Counting the number of turns in a solution or section
    return len(solution.split())

def process_file(file_path):
    with open(file_path, 'r') as file:
        solutions = file.readlines()

    file_data = []
    total_turns = []
    section_turns = [[] for _ in range(4)]  # Assuming four sections per solution

    for solution in solutions:
        sections = solution.split('|')
        if len(sections) != 4:
            continue  # Skip this solution

        section_counts = [count_turns(section) for section in sections]
        total_count = sum(section_counts)
        file_data.append((total_count, section_counts))

        total_turns.append(total_count)
        for i, count in enumerate(section_counts):
            section_turns[i].append(count)

    # Calculate expected values (means), standard deviations and variances
    expected_total = np.mean(total_turns)
    std_dev_total = np.std(total_turns)
    var_total = np.var(total_turns)

    expected_sections = [np.mean(section) for section in section_turns]
    std_dev_sections = [np.std(section) for section in section_turns]
    var_sections = [np.var(section) for section in section_turns]

    return file_data, expected_total, std_dev_total, var_total, expected_sections, std_dev_sections, var_sections




folder_path = './Solutions'
all_data = {}

# Sort the file names using the natural sort key
sorted_files = sorted(os.listdir(folder_path), key=natural_sort_key)

for file_name in sorted_files:
    if file_name.endswith('.txt'):
        file_path = os.path.join(folder_path, file_name)
        # Update here to unpack all returned values
        data, expected_total, std_dev_total, var_total, expected_sections, std_dev_sections, var_sections = process_file(file_path)
        all_data[file_name] = data

        # Print statements (or any other processing you want to do)
        # print(f'Expected total for {file_name}: {expected_total}, Std Dev: {std_dev_total}, Variance: {var_total}')
        # for i, (exp, std_dev, var) in enumerate(zip(expected_sections, std_dev_sections, var_sections)):
        #     print(f'Expected value for Section {i+1} in {file_name}: {exp}, Std Dev: {std_dev}, Variance: {var}')

# all_data now contains the count of turns for each solution and its sections, grouped by file

# Define bin edges for total turns
bin_edges_total = range(0, 103, 3)

# Maximum y-axis value
max_y_value_total = 0.08  # Adjust based on your data
max_y_value_subsections = 0.25  # Adjust based on your data

colors = ['red', 'orange', 'green', 'blue']  # Colors for the four sections

for file_name, data in all_data.items():
    total_counts = [d[0] for d in data]
    section_counts = [list(zip(*[d[1] for d in data]))[i] for i in range(4)]

    plt.figure(figsize=(12, 10))  # Adjusted figure size for the layout

    # Define GridSpec layout
    gs = gridspec.GridSpec(2, 1, height_ratios=[70, 30])  # 70% to the top plot, 30% to the bottom

    # Main "Totals" Plot
    ax0 = plt.subplot(gs[0])
    ax0.hist(total_counts, bins=bin_edges_total, color='black', alpha=0.7, density=True)
    ax0.set_title(f'PMF of Total Turns for {file_name}')
    ax0.set_xlabel('Number of Turns')
    ax0.set_ylabel('Probability')
    ax0.set_ylim(0, max_y_value_total)

    # Smaller Subsection Plots with different bin ranges
    section_names = ['Cross', 'F2L', 'OLL', 'PLL']  # Section names
    ax1 = plt.subplot(gs[1])
    for i, section in enumerate(section_counts):
        # Define bin edges based on the section
        bin_edges_subsections = range(0, 60, 1)
        ax1.hist(section, bins=bin_edges_subsections, color=colors[i], alpha=0.7, label=section_names[i], density=True)

    ax1.set_title('PMF of Section Turns')
    ax1.set_xlabel('Number of Turns')
    ax1.set_ylabel('Probability')
    ax1.set_ylim(0, max_y_value_subsections)
    ax1.legend()

    plt.tight_layout()
    plt.show()



# Define columns for each DataFrame
expected_columns = ['File', 'Expected Total'] + [f'Expected {name}' for name in section_names]
std_dev_columns = ['File', 'Std Dev Total'] + [f'Std Dev {name}' for name in section_names]
variance_columns = ['File', 'Variance Total'] + [f'Variance {name}' for name in section_names]

# Create DataFrames
expected_df = pd.DataFrame(columns=expected_columns)
std_dev_df = pd.DataFrame(columns=std_dev_columns)
variance_df = pd.DataFrame(columns=variance_columns)

# Fill the DataFrames with your data
for file_name in all_data.keys():
    file_path = os.path.join(folder_path, file_name)
    data, expected_total, std_dev_total, var_total, expected_sections, std_dev_sections, var_sections = process_file(file_path)

    # Create rows for each DataFrame
    expected_row = [file_name, expected_total] + expected_sections
    std_dev_row = [file_name, std_dev_total] + std_dev_sections
    variance_row = [file_name, var_total] + var_sections

    # Add rows to each DataFrame
    expected_df.loc[len(expected_df)] = expected_row
    std_dev_df.loc[len(std_dev_df)] = std_dev_row
    variance_df.loc[len(variance_df)] = variance_row

# Display the DataFrames
print("Expected Values:")
print(expected_df)
print("\nStandard Deviations:")
print(std_dev_df)
print("\nVariances:")
print(variance_df)
