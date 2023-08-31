from scraper import *

# Mock HTML content for testing purposes
mock_html = """
<div class="career-search-component__content--items">
    <a href="https://example.com/job1">
        <span class="career-search-component__item--date">Today</span>
        <h4 class="title">Job 1</h4>
        <span class="career-search-component__item--meta__segment"><strong>Location</strong>: City A</span>
        <span class="career-search-component__item--meta__segment"><strong>Business segment</strong>: Segment A</span>
    </a>
    <a href="https://example.com/job2">
        <span class="career-search-component__item--date">Yesterday</span>
        <h4 class="title">Job 2</h4>
        <span class="career-search-component__item--meta__segment"><strong>Location</strong>: City B</span>
        <span class="career-search-component__item--meta__segment"><strong>Business segment</strong>: Segment B</span>
    </a>
</div>
"""

# Creating unit tests for the scraper
import unittest

class TestScraper(unittest.TestCase):
    
    def test_extract_job_details(self):
        soup = BeautifulSoup(mock_html, 'html.parser')
        job_cards = [child for child in soup.children if child.name]
        
        # Test the first job card
        job1 = {
            'posting_date': 'Today',
            'title': 'Job 1',
            'Location': 'City A',
            'Business segment': 'Segment A',
            'link': 'https://example.com/job1'
        }
        self.assertEqual(extract_job_details(job_cards[0]), job1)
        
        # Test the second job card
        job2 = {
            'posting_date': 'Yesterday',
            'title': 'Job 2',
            'Location': 'City B',
            'Business segment': 'Segment B',
            'link': 'https://example.com/job2'
        }
        self.assertEqual(extract_job_details(job_cards[1]), job2)

