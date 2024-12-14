from fetch_advent_input import fetch_advent_input
import re
import numpy as np

example_input = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""
example1_result = 18

def solve(input_string: str) -> int:
    result = 0
    # Step 1: Convert the input string into a 2D grid
    grid = [list(line.strip()) for line in input_string.strip().split('\n')]

    # Convert the grid to a numpy array for easier manipulation
    grid_array = np.array(grid)

    # Function to rotate the grid by 45 degrees
    def rotate_grid_45(grid):
        max_rows, max_cols = grid.shape
        rotated_grid = []

        # There are (max_rows + max_cols - 1) diagonals
        for diag in range(max_rows + max_cols - 1):
            rotated_row = []
            for row in range(max_rows):
                col = diag - row
                if 0 <= col < max_cols:
                    rotated_row.append(grid[row, col])
            if rotated_row:
                rotated_grid.append(rotated_row)
        return np.array(rotated_grid, dtype=object)

    for i in range(0,3):
        for row_id in range(0, len(grid_array)):
            row = ''.join(grid_array[row_id])
            pattern = r"XMAS"
            matches = re.findall(pattern, row)
            result += len(matches)
        #rotate input
        grid_array = rotate_grid_45(grid_array)

    return result    
  

# Test the example
result = solve(example_input)
if result == example1_result:
    print()
    print("The example result matches the expected result.")
    print()
else:
    print()
    print("The example result does not match the expected result. Got:", result, "Expected:", example1_result)
    print()

# Call the function and get the problem input
problem_input = fetch_advent_input(4)

if problem_input:
    problem_input = problem_input.strip()
    # Use the problem_input variable as needed
    result = solve(problem_input)
    print()
    print("The result of this Part is:", result)
    print()