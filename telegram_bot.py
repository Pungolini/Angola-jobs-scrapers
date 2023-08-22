import requests
from decouple import config

TELEGRAM_TOKEN = config('TELEGRAM_API_TOKEN')
CHAT_ID = config('TELEGRAM_CHAT_ID')



def send_telegram_message(job_postings):
    # Define the base URL for the Telegram Bot API
    base_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    # Format the message using the provided template
    message = "📢 New Job Postings at Standard Bank!\n\n"
    for job in job_postings:
        message += "----------------------\n"
        message += f"🔹 **Title**: {job['title']}\n"
        message += f"📅 **Posting Date**: {job['posting_date']}\n"
        message += f"📍 **Location**: {job['Location']}\n"
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