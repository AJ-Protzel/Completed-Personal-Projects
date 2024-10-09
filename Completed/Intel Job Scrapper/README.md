# Job Data Scraper and Filter

This Python script is designed to scrape job data from a list of URLs and save the data in a CSV file. It also includes a filtering mechanism to exclude certain records based on specified conditions. The script utilizes the `requests` library for making HTTP requests, the `BeautifulSoup` library for parsing HTML content, and the `csv` library for reading and writing CSV files.

## Prerequisites

Before running the script, make sure you have the following prerequisites installed:

- Python 3.x
- `requests` library (`pip install requests`)
- `beautifulsoup4` library (`pip install beautifulsoup4`)

## Usage

1. Clone the repository or download the script file (`job_scraper.py`) to your local machine.

2. Create a file named `job_urls.txt` and populate it with the URLs of the job pages you want to scrape. Each URL should be on a separate line.

3. Open a terminal or command prompt and navigate to the directory where the script file is located.

4. Run the script by executing the following command:

5. The script will start scraping the job data from each URL and save it in a CSV file named `job_data.csv`.

6. Once the scraping is complete, the script will clean the data by filtering out certain records based on predefined conditions. The filtered data will be written back to `job_data.csv`.

7. The final filtered data can be found in `job_data.csv`.

## Customization

If you want to customize the filtering conditions, you can modify the following variables in the script:

- `keywords`: A list of keywords. Records with titles containing any of these keywords will be excluded from the final filtered data.
- `exclude_word`: A single word. Records with titles that also contain this word will be included in the final filtered data, even if they match the keywords.

Feel free to modify the code to suit your specific requirements.

## License

This project is licensed under the [MIT License](LICENSE).
