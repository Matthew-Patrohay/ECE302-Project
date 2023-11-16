#!/bin/bash

# # Path to the input file with scrambles
# SCRAMBLES_FILE="scrambles.txt"

# # Path to the output file for results
# OUTPUT_FILE="results.txt"

# # Clear the output file
# > "$OUTPUT_FILE"

# # Loop through each line in the scrambles file
# while IFS= read -r scramble
# do
#     # Run the solver command and append the output to the results file
#     # echo "Processing scramble: $scramble" >> "$OUTPUT_FILE"
#     bin/solver -d data/ -t "$scramble" >> "$OUTPUT_FILE"
#     echo "---------------------------------------" >> "$OUTPUT_FILE"
# done < "$SCRAMBLES_FILE"




#!/bin/bash

# # Path to the input file with scrambles
# SCRAMBLES_FILE="scrambles.txt"

# # Path to the output file for results
# OUTPUT_FILE="results.txt"

# # Clear the output file
# > "$OUTPUT_FILE"

# # Loop through each line in the scrambles file
# while IFS= read -r scramble
# do
#     # Run the solver command, replace double spaces with single spaces, and append the output to the results file
#     bin/solver -d data/ -t "$scramble" | sed 's/  */ /g' >> "$OUTPUT_FILE"
#     # echo "---------------------------------------" >> "$OUTPUT_FILE"
# done < "$SCRAMBLES_FILE"



#!/bin/bash

# Directory containing the scramble files
SCRAMBLES_DIR="scrambles"

# Iterate over each .txt file in the scrambles directory
for SCRAMBLES_FILE in "$SCRAMBLES_DIR"/*.txt
do
    # Extract the base name of the file without the extension
    BASE_NAME=$(basename "$SCRAMBLES_FILE" .txt)

    # Define the output file name
    OUTPUT_FILE="${SCRAMBLES_DIR}/${BASE_NAME}_solutions.txt"

    # Clear the output file
    > "$OUTPUT_FILE"

    # Loop through each line in the scrambles file
    while IFS= read -r scramble
    do
        # Run the solver command, replace double spaces with single spaces, and append the output to the results file
        bin/solver -d data/ -t "$scramble" | sed 's/  */ /g' >> "$OUTPUT_FILE"
        # echo "---------------------------------------" >> "$OUTPUT_FILE"
    done < "$SCRAMBLES_FILE"
done
