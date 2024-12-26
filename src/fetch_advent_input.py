import os
import requests
from datetime import datetime

def fetch_advent_input(day: int = None) -> str:
    # Determine the day of December to fetch
    #day = current_date.day if 1 <= current_date.day <= 25 and current_date.month == 12 else 1

    # Define the URL to fetch
    url = f'https://adventofcode.com/2024/day/{day}/input'
    output_file = f'202412{day}_input.txt'

    # Check if the output file already exists
    if os.path.exists(output_file):
        print(f"{output_file} already exists. Reading content from the file.")
        with open(output_file, 'r') as file:
            problem_input = file.read()
    else:
        # Read the session cookie from the file
        with open('session.cookie', 'r') as file:
            session_cookie = file.read().strip()

        # Set up the cookies dictionary
        cookies = {'session': session_cookie}

        # Make the GET request with the session cookie
        response = requests.get(url, cookies=cookies)

        # Check if the request was successful
        if response.status_code == 200:
            print("Request successful!")
            problem_input = response.text

            # Write the content to the output file
            with open(output_file, 'w') as file:
                file.write(problem_input)
        else:
            print(f"Failed to fetch {url}. Status code: {response.status_code}")
            problem_input = None

    return problem_input