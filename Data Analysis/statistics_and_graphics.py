import os
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def count_turns(solution):
    # Counting the number of turns in a solution or section
    return len(solution.split())

def process_file(file_path):
    with open(file_path, 'r') as file:
        solutions = file.readlines()

    file_data = []
    for solution in solutions:
        sections = solution.split('|')
        section_counts = [count_turns(section) for section in sections]
        total_count = sum(section_counts)
        file_data.append((total_count, section_counts))
    
    return file_data

folder_path = './Solutions'
all_data = {}

for file_name in os.listdir(folder_path):
    if file_name.endswith('.txt'):
        file_path = os.path.join(folder_path, file_name)
        all_data[file_name] = process_file(file_path)

# all_data now contains the count of turns for each solution and its sections, grouped by file

# Define bin edges for total turns
bin_edges_total = range(0, 103, 3)

# Maximum y-axis value
max_y_value_total = 200  # Adjust based on your data
max_y_value_subsections = 250  # Adjust based on your data

colors = ['red', 'orange', 'green', 'blue']  # Colors for the four sections

for file_name, data in all_data.items():
    total_counts = [d[0] for d in data]
    section_counts = [list(zip(*[d[1] for d in data]))[i] for i in range(4)]

    plt.figure(figsize=(12, 10))  # Adjusted figure size for the layout

    # Define GridSpec layout
    gs = gridspec.GridSpec(2, 1, height_ratios=[70, 30])  # 70% to the top plot, 30% to the bottom

    # Main "Totals" Plot
    ax0 = plt.subplot(gs[0])
    ax0.hist(total_counts, bins=bin_edges_total, color='black', alpha=0.7)
    ax0.set_title(f'Total Turns for {file_name}')
    ax0.set_xlabel('Number of Turns')
    ax0.set_ylabel('Frequency')
    ax0.set_ylim(0, max_y_value_total)

    # Smaller Subsection Plots with different bin ranges
    ax1 = plt.subplot(gs[1])
    for i, section in enumerate(section_counts):
        # Define bin edges based on the section
        bin_edges_subsections = range(0, 60, 1)
        ax1.hist(section, bins=bin_edges_subsections, color=colors[i], alpha=0.7, label=f'Section {i + 1}')

    ax1.set_title('Section Turns Distribution')
    ax1.set_xlabel('Number of Turns')
    ax1.set_ylabel('Frequency')
    ax1.set_ylim(0, max_y_value_subsections)
    ax1.legend()

    plt.tight_layout()
    plt.show()


