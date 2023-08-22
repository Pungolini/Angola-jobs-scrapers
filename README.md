# Standard Bank Job Postings Scraper

This repository contains a script to automatically scrape and monitor job postings from the Standard Bank website.

## Overview

The script checks the Standard Bank job postings page at regular intervals and sends alerts for new postings via Telegram. The primary goal is to keep users informed about new job opportunities without manually checking the website.

## How It Works

1. The script fetches the job postings webpage using the `requests` library.
2. It then parses the content with `BeautifulSoup` to extract relevant job details.
3. The extracted job postings are compared with previously saved postings.
4. If new postings are detected, an alert is sent via Telegram using a bot.

## Tools & Technologies

- **Development**:
  - Python: Main programming language used.
  - BeautifulSoup: For parsing and extracting data from the website.
  - pandas: For data manipulation and comparison.
  - python-decouple: For managing environment variables.
  
- **Deployment**:
  - GitHub Actions: Automates the script to run at defined intervals.
  - Telegram Bot API: Sends alerts to users.

## Setup & Usage

1. Clone this repository.
2. Install the required Python libraries.
3. Set up a Telegram bot and obtain the API token and chat ID.
4. If running locally, use an `.env` file for environment variables or set them up in your environment.
5. For automated runs, configure the provided GitHub Actions workflow.

---

Developed with 💙 by [Mauro Pungo](https://www.linkedin.com/in/mauro-pungo).
