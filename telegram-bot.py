#%%
import requests
from bs4 import BeautifulSoup
import pandas as pd
import argparse
import os
from companies_scrapers import *

#%%

# Constants
CSV_PATH = "standard_bank_job_postings.csv"
TELEGRAM_TOKEN = "6696100166:AAGxzhVTLqtjLwLuAOQVtvFHUDy5j2G2d6g"#os.environ['TELEGRAM_API_TOKEN']
CHAT_ID = "6206009875"#os.environ['TELEGRAM_CHAT_ID']

#%%

def get_emoji(text):

    emoji = "🔹"

    if "loc" in text.lower():
        emoji = "📍"
    elif "tit" in text.lower():
        emoji = "🔹"
    elif "link" in text.lower():
        emoji = "💻"
    elif "dat" in text.lower():
        emoji = "📅"
    
    return emoji


        

def send_telegram_message(jobs_df,company = None):
    # Define the base URL for the Telegram Bot API
    base_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    # Format the message using the provided template
    message = f"📢 New Job Postings {'at' + company if company else ''}!\n\n"

    for job_idx in jobs_df.index:
        print(job_idx)
        message += "-"*40 + "\n"

        for field in jobs_df.columns:
            emoji = get_emoji(field)
            message += f"{emoji} **{field}**: {jobs_df[field][job_idx]}\n"
        message += "-"*40 + "\n\n"

    message += f"Total new postings: {len(jobs_df)}"

    print(message)
    
    # Send the message using the Telegram Bot API
    response = requests.post(base_url, data={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
    return response.json()

# Sample usage (you can uncomment and test with your API token and chat ID):
# sample_jobs = [{"title": "Sample Job", "posting_date": "Today", "Location": "City", "Business segment": "Segment", "Type of Employment": "Full-time", "link": "https://example.com"}]
# send_telegram_message(sample_jobs)


def check_new_postings(extracted_jobs_df):


    # If there are no jobs listed, do nothing
    if extracted_jobs is None:
        return False
    # Convert to DataFrame
    df_new_jobs = extracted_jobs_df
    
    # Check if the CSV file exists, if not, create an empty DataFrame
    if os.path.exists(CSV_PATH):
        df_saved_jobs = pd.read_csv(CSV_PATH)
    else:
        df_saved_jobs = pd.DataFrame(columns=extracted_jobs_df.columns)


    # Compare the two DataFrames to find new postings
    ref_field = extracted_jobs_df.columns[0]
    
    new_postings = df_new_jobs[~df_new_jobs[ref_field].isin(df_saved_jobs[ref_field])]

    # If there are new postings, print an alert
    if not new_postings.empty:
        print(f"ALERT: {len(new_postings)} new job postings found!")
        send_telegram_message(new_postings)


        # Save the updated DataFrame to the CSV
        df_new_jobs.to_csv(CSV_PATH, index=False)
    else:
        print("No new job postings found.")

if __name__ == "__main__":

    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="Monitorização automática de vagas de trabalho")
    parser.add_argument('--Empresa',type=str, default="Azule",help = f"Nome da empresa. Atualmente disponíveis: {','.join(list(AVAILABLE_COMPANIES))}")
    parser.add_argument('--verbose',type=bool, default=False)
    args = parser.parse_args()


    extracted_jobs = get_jobs_Azule(verbose = args.verbose)

    check_new_postings(extracted_jobs)
# %%
