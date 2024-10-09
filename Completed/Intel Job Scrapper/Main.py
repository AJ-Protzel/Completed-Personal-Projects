import csv
import requests
from bs4 import BeautifulSoup

# Define the filename for the input file containing the URLs
input_filename = 'job_urls.txt'

# Read the URLs from the input file into a list
with open(input_filename, 'r', encoding='utf-8') as file:
    urls = [line.strip() for line in file]

# Define the filename for the CSV file
output_filename = 'job_data.csv'

# Open the file in write mode and create a CSV writer object with explicit encoding
with open(output_filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Write the header row to the CSV file
    writer.writerow(['Title', 'Location', 'Mode', 'Description', 'Qualifications', 'URL'])

    print("Reading in all job data")

    # Iterate over the URLs
    for url in urls:
        # get main html soup
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # get each element
        title = soup.find('h1').text.strip()
        location = soup.find('span', {'class':'job-description__location-pin job-info'}).text.strip()
        mode = soup.find('span', {'class':'job-category-info job-info'}).text.strip()
        description = soup.find('div', {'class': 'ats-description'}).text.strip()

        # split large description
        qualifications = description[description.index("Qualifications") + len("Qualifications"):description.index("Inside this Business Group")].strip()
        description = description[description.index("Job Description") + len("Job Description"):description.index("Qualifications")].strip()
        
        # Write the data for each URL to the CSV file
        writer.writerow([title, location, mode, description, qualifications, url])

print("All job data gathered and saved in", output_filename)
print("Cleaning all job data")

# Remove records based on specified conditions
filtered_rows = []
with open(output_filename, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row) > 0:
            first_column = row[0].lower()
            # remove records whose titles contain:
            keywords = ["chemistry", "chemical", "physics", "mechanical", "senior", "sr."]
            # exclude if titles also contain:
            exclude_word = "computer science"
            if not any(keyword in first_column for keyword in keywords):
                filtered_rows.append(row)

with open(output_filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(filtered_rows)

print('Filtered records have been written to', output_filename)