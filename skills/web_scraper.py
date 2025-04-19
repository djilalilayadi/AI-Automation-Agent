import requests
from bs4 import BeautifulSoup
from typing import List, Dict

class WebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
    
    def scrape_jobs(self, url: str) -> List[Dict]:
        """Basic job posting scraper"""
        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # These selectors need to be customized per site
            jobs = []
            for job in soup.select('.job-listing'):  # Example selector
                jobs.append({
                    'title': job.select_one('.title').text.strip(),
                    'company': job.select_one('.company').text.strip(),
                    'location': job.select_one('.location').text.strip(),
                    'url': url
                })
            return jobs
        
        except Exception as e:
            print(f"Scraping failed: {e}")
            return []