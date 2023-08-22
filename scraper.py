import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import argparse
import os
from telegram_bot import send_telegram_message


# Set up command line argument parsing
parser = argparse.ArgumentParser(description="Scrape job postings from a given URL.")
parser.add_argument('--url', type=str, default="https://www.standardbank.com/sbg/standard-bank-group/careers/apply/jobs/view-all-jobs", help="URL to scrape job postings from.")
args = parser.parse_args()

# Constants
URL = args.url
CSV_PATH = "standard_bank_job_postings.csv"
TELEGRAM_TOKEN = os.environ['TELEGRAM_API_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']

def scrape_job_postings():
    # Fetch the web page
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract job listings
    job_listings_div = soup.find('div', class_='career-search-component__content--items')
    job_cards = [child for child in job_listings_div.children if child.name]

    # Extract job details
    def extract_job_details(job_card):
        job_details = {}
        job_details['posting_date'] = job_card.find('span', class_='career-search-component__item--date').get_text(strip=True)
        title_element = job_card.find('h4', class_='title')
        job_details['title'] = title_element.get_text(strip=True) if title_element else None
        meta_segments = job_card.find_all('span', class_='career-search-component__item--meta__segment')
        for segment in meta_segments:
            key = segment.find('strong').get_text(strip=True).rstrip(':')
            value = segment.get_text(strip=True).replace(key + ':', '').strip()
            job_details[key] = value
        job_details['link'] = job_card['href']
        return job_details

    extracted_jobs = [extract_job_details(job_card) for job_card in job_cards if job_card.name == 'a']
    return extracted_jobs

def check_new_postings(extracted_jobs):
    # Convert to DataFrame
    df_new_jobs = pd.DataFrame(extracted_jobs)
    
    # Load the saved CSV data
    df_saved_jobs = pd.read_csv(CSV_PATH)

    # Compare the two DataFrames to find new postings
    new_postings = df_new_jobs[~df_new_jobs['link'].isin(df_saved_jobs['link'])]

    # If there are new postings, print an alert
    if not new_postings.empty:
        print(f"ALERT: {len(new_postings)} new job postings found!")
        send_telegram_message(new_postings)

        # Save the updated DataFrame to the CSV
        df_new_jobs.to_csv(CSV_PATH, index=False)
    else:
        print("No new job postings found.")

if __name__ == "__main__":
    extracted_jobs = scrape_job_postings()
    check_new_postings(extracted_jobs)