import csv
from bs4 import BeautifulSoup

filename = 'bcs33'

# Open the HTML file and parse it with BeautifulSoup
with open(f'{filename}.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

mcqs = []

rows = soup.find_all('tr')

current_question = None

for row in rows:
    # Get all the columns (cells) in the row
    cells = row.find_all('td')
    
    # Check if the row contains a question (spanning multiple columns)
    if len(cells) == 1 and cells[0].has_attr('colspan'):
        current_question = cells[0].get_text(strip=True)
    
    # Check if the row contains answer options
    elif len(cells) >= 2:  # Adjusted to handle cases where there are more than 4 options
        options = []
        correct_answer = None
        
        for cell in cells:
            option_text = cell.get_text(strip=True)
            
            # Check if this option is the correct answer
            if cell.find('strong'):
                correct_answer = option_text
            
            options.append(option_text)
        
        # Ensure options list has exactly 4 elements
        while len(options) < 4:
            options.append('')  # Fill in empty cells if fewer than 4 options
            
        # Default to 1 point for each question; adjust as needed
        points = 1
        
        # Store the question, options, correct answer, and points in the list
        mcqs.append({
            'question': current_question,
            'options': options,
            'correct_answer': correct_answer,
            'points': points
        })

# Save the extracted MCQs to a CSV file
output_path = f'filtered_mcqs/{filename}.csv'

# Ensure the output directory exists
import os
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    
    # Write the header
    writer.writerow(['Question', 'Option 1', 'Option 2', 'Option 3', 'Option 4', 'Correct Answer', 'Points'])
    
    # Write the data
    for mcq in mcqs:
        writer.writerow([mcq['question']] + mcq['options'] + [mcq['correct_answer'], mcq['points']])

print(f"MCQs have been extracted and saved as CSV to {output_path}")
