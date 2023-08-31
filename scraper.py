import requests
from bs4 import BeautifulSoup
import pandas as pd
import argparse
import os

# Constants
URL = "https://www.standardbank.com/sbg/standard-bank-group/careers/apply/jobs/view-all-jobs"
CSV_PATH = "standard_bank_job_postings.csv"
TELEGRAM_TOKEN = "6696100166:AAGxzhVTLqtjLwLuAOQVtvFHUDy5j2G2d6g"#os.environ['TELEGRAM_API_TOKEN']
CHAT_ID = "6206009875"#os.environ['TELEGRAM_CHAT_ID']


def send_telegram_message(job_postings):
    # Define the base URL for the Telegram Bot API
    base_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    # Format the message using the provided template
    message = "📢 New Job Postings at Standard Bank!\n\n"
    for job in job_postings:
        message += "----------------------\n"
        # message += f"🔹 **Title**: {job['title']}\n"
        # message += f"📅 **Posting Date**: {job['posting_date']}\n"
        # message += f"📍 **Location**: {job['Location']}\n"
        message += f"🔍 **Business Segment**: {job['Business segment']}\n"
        message += f"📝 **Type of Employment**: {job['Type of Employment']}\n"
        message += f"🔗 {job['link']}\n"
        message += "----------------------\n\n"

    
    message += f"Total new postings: {len(job_postings)}"
    
    # Send the message using the Telegram Bot API
    response = requests.post(base_url, data={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
    return response.json()

# Sample usage (you can uncomment and test with your API token and chat ID):
# sample_jobs = [{"title": "Sample Job", "posting_date": "Today", "Location": "City", "Business segment": "Segment", "Type of Employment": "Full-time", "link": "https://example.com"}]
# send_telegram_message(sample_jobs)

# Extract job details
def extract_job_details(job_card):
    job_details = {}
    
    # # Extract posting_date
    # posting_date_element = job_card.find('span', class_='career-search-component__item--date')
    # job_details['posting_date'] = posting_date_element.get_text(strip=True) if posting_date_element else None
    
    # # Extract title
    # title_element = job_card.find('h4', class_='title')
    # job_details['title'] = title_element.get_text(strip=True) if title_element else None
    
    # Extract meta segments
    meta_segments = job_card.find_all('span', class_='career-search-component__item--meta__segment')
    for segment in meta_segments:
        key_element = segment.find('strong')
        key = key_element.get_text(strip=True).rstrip(':') if key_element else None
        value = segment.get_text(strip=True).replace(f"{key}:", '').strip() if key else None
        if key:
            job_details[key] = value
    
    # Extract link
    job_details['link'] = job_card['href']
    
    return job_details

    
def scrape_job_postings():
    # Fetch the web page
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract job listings
    job_listings_div = soup.find('div', class_='career-search-component__content--items')
    job_cards = [child for child in job_listings_div.children if child.name]

    print(f"{len(job_cards)} job cards")

    extracted_jobs = [extract_job_details(job_card) for job_card in job_cards if job_card.name == 'a']
    return extracted_jobs

def check_new_postings(extracted_jobs):
    # Convert to DataFrame
    df_new_jobs = pd.DataFrame(extracted_jobs)
    
    # Check if the CSV file exists, if not, create an empty DataFrame
    if os.path.exists(CSV_PATH):
        df_saved_jobs = pd.read_csv(CSV_PATH)
    else:
        columns = ['Location', 'Business segment', 'link'] #,'posting_date', 'title', 
        df_saved_jobs = pd.DataFrame(columns=columns)

    # Compare the two DataFrames to find new postings
    new_postings = df_new_jobs[~df_new_jobs['link'].isin(df_saved_jobs['link'])]

    # If there are new postings, print an alert
    if not new_postings.empty:
        print(f"ALERT: {len(new_postings)} new job postings found!")
        send_telegram_message(new_postings.to_dict('records'))


        # Save the updated DataFrame to the CSV
        df_new_jobs.to_csv(CSV_PATH, index=False)
    else:
        print("No new job postings found.")

if __name__ == "__main__":

    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="Scrape job postings from a given URL.")
    parser.add_argument('--url', type=str, default=URL, help="URL to scrape job postings from.")
    args = parser.parse_args()
    URL = args.url
    
    extracted_jobs = scrape_job_postings()
    check_new_postings(extracted_jobs)