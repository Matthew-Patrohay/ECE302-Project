from pyTwistyScrambler import scrambler333
import random

# Initialize an empty list to store scrambles
scrambles = []

def general_random_scramble():
    random_array_scramble = []
    turn_set = ["R", "R'", "R2", "L", "L'", "L2", "U", "U'", "U2", "D", "D'", "D2", "F", "F'", "F2", "B", "B'", "B2"]
    for _ in range(40):
        random_array_scramble.append(random.choice(turn_set))
    return ' '.join(random_array_scramble)


def smart_random_scramble():
    random_array_scramble = []
    turn_set = ["R", "R'", "R2", "L", "L'", "L2", "U", "U'", "U2", "D", "D'", "D2", "F", "F'", "F2", "B", "B'", "B2"]
    
    last_face = None
    second_last_face = None
    for _ in range(40):
        valid_turns = [turn for turn in turn_set if turn[0] != last_face]

        if second_last_face == 'F' and last_face == 'B':
            valid_turns = [turn for turn in valid_turns if turn[0] != 'F']
        elif second_last_face == 'B' and last_face == 'F':
            valid_turns = [turn for turn in valid_turns if turn[0] != 'B']
        elif second_last_face == 'R' and last_face == 'L':
            valid_turns = [turn for turn in valid_turns if turn[0] != 'R']
        elif second_last_face == 'L' and last_face == 'R':
            valid_turns = [turn for turn in valid_turns if turn[0] != 'L']
        elif second_last_face == 'U' and last_face == 'D':
            valid_turns = [turn for turn in valid_turns if turn[0] != 'U']
        elif second_last_face == 'D' and last_face == 'U':
            valid_turns = [turn for turn in valid_turns if turn[0] != 'D']

        selected_turn = random.choice(valid_turns)
        random_array_scramble.append(selected_turn)

        # Update second_last_face and last_face for the next iteration
        second_last_face = last_face
        last_face = selected_turn[0]

    return ' '.join(random_array_scramble)

# Generate 100 scrambles
for each in range(1000):
    # scramble = scrambler333.get_WCA_scramble()
    scramble = general_random_scramble()
    # scramble = smart_random_scramble()
    print(scramble)
    scrambles.append(scramble)

# Write scrambles to a text file
with open('1000_random_length_40.txt', 'w') as file:
    for scramble in scrambles:
        file.write(scramble + '\n')