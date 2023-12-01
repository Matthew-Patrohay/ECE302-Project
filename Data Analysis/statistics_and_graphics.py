import os
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd
import re

# Set font sizes globally
plt.rcParams.update({'font.size': 14})
plt.rcParams['axes.titlesize'] = 22
plt.rcParams['axes.labelsize'] = 22
plt.rcParams['xtick.labelsize'] = 18
plt.rcParams['ytick.labelsize'] = 18
plt.rcParams['legend.fontsize'] = 18


def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

def count_turns(solution):
    return len(solution.split())

def process_file(file_path):
    with open(file_path, 'r') as file:
        solutions = file.readlines()

    file_data = []
    total_turns = []
    section_turns = [[] for _ in range(4)]

    for solution in solutions:
        sections = solution.split('|')
        if len(sections) != 4:
            continue

        section_counts = [count_turns(section) for section in sections]
        total_count = sum(section_counts)
        file_data.append((total_count, section_counts))

        total_turns.append(total_count)
        for i, count in enumerate(section_counts):
            section_turns[i].append(count)

    expected_total = np.mean(total_turns)
    std_dev_total = np.std(total_turns)
    var_total = np.var(total_turns)

    expected_sections = [np.mean(section) for section in section_turns]
    std_dev_sections = [np.std(section) for section in section_turns]
    var_sections = [np.var(section) for section in section_turns]

    return file_data, expected_total, std_dev_total, var_total, expected_sections, std_dev_sections, var_sections

folder_path = './Solutions'
all_data = {}

sorted_files = sorted(os.listdir(folder_path), key=natural_sort_key)

for file_name in sorted_files:
    if file_name.endswith('.txt'):
        file_path = os.path.join(folder_path, file_name)
        data, expected_total, std_dev_total, var_total, expected_sections, std_dev_sections, var_sections = process_file(file_path)
        all_data[file_name] = data

bin_edges_total = range(0, 103, 3)

max_y_value_total = 0.06
max_y_value_subsections = 0.25

colors = ['red', 'orange', 'green', 'blue']

for file_name, data in all_data.items():
    total_counts = [d[0] for d in data]
    section_counts = [list(zip(*[d[1] for d in data]))[i] for i in range(4)]

    plt.figure(figsize=(14, 7))

    gs = gridspec.GridSpec(2, 1, height_ratios=[60, 40])

    ax0 = plt.subplot(gs[0])
    ax0.hist(total_counts, bins=bin_edges_total, color='black', alpha=0.7, density=True)
    ax0.set_title(f'PMF of Total Turns for {file_name}')
    ax0.set_xlabel('Number of Turns')
    ax0.set_ylabel('Probability')
    ax0.set_ylim(0, max_y_value_total)

    section_names = ['Cross', 'F2L', 'OLL', 'PLL']
    ax1 = plt.subplot(gs[1])
    for i, section in enumerate(section_counts):
        bin_edges_subsections = range(0, 60, 1)
        ax1.hist(section, bins=bin_edges_subsections, color=colors[i], alpha=0.7, label=section_names[i], density=True)

    ax1.set_title('PMF of Section Turns')
    ax1.set_xlabel('Number of Turns')
    ax1.set_ylabel('Probability')
    ax1.set_ylim(0, max_y_value_subsections)
    ax1.legend()

    plt.tight_layout()
    plt.show()

expected_columns = ['File', 'Expected Total'] + [f'Expected {name}' for name in section_names]
std_dev_columns = ['File', 'Std Dev Total'] + [f'Std Dev {name}' for name in section_names]
variance_columns = ['File', 'Variance Total'] + [f'Variance {name}' for name in section_names]

expected_df = pd.DataFrame(columns=expected_columns)
std_dev_df = pd.DataFrame(columns=std_dev_columns)
variance_df = pd.DataFrame(columns=variance_columns)

for file_name in all_data.keys():
    file_path = os.path.join(folder_path, file_name)
    data, expected_total, std_dev_total, var_total, expected_sections, std_dev_sections, var_sections = process_file(file_path)

    expected_row = [file_name, expected_total] + expected_sections
    std_dev_row = [file_name, std_dev_total] + std_dev_sections
    variance_row = [file_name, var_total] + var_sections

    expected_df.loc[len(expected_df)] = expected_row
    std_dev_df.loc[len(std_dev_df)] = std_dev_row
    variance_df.loc[len(variance_df)] = variance_row

print("Expected Values:")
print(expected_df)
print("\nStandard Deviations:")
print(std_dev_df)
print("\nVariances:")
print(variance_df)
