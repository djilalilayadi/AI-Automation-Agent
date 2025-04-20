import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
from core.task_runner import BaseTask

class WebsiteScraper(BaseTask):
    def __init__(self, **params):
        super().__init__(**params)
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AutomationPortfolio/1.0"
        self.request_delay = params.get('request_delay', 2)
        self.respect_robots = params.get('respect_robots', True)
        
    def check_robots_txt(self, url):
        if not self.respect_robots:
            return True
            
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        
        rp = RobotFileParser()
        try:
            rp.set_url(robots_url)
            rp.read()
            return rp.can_fetch(self.user_agent, url)
        except Exception:
            # If robots.txt can't be read, proceed but be cautious
            return True

    def execute(self):
        # Check robots.txt first
        if not self.check_robots_txt(self.params['url']):
            raise Exception(f"Scraping disallowed by robots.txt for {self.params['url']}")

        headers = {'User-Agent': self.user_agent}
        
        try:
            # Initial request
            response = requests.get(
                self.params['url'],
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            
            # Parse content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract data
            results = []
            items = soup.select(self.params['item_selector'])
            
            for i, item in enumerate(items):
                result = {}
                for field, selector in self.params['field_selectors'].items():
                    element = item.select_one(selector)
                    result[field] = element.text.strip() if element else None
                results.append(result)
                
                # Respect delay between items (if multiple pages needed)
                if i < len(items) - 1:
                    time.sleep(self.request_delay)
            
            # Save results
            output_dir = 'outputs/scraped_data'
            os.makedirs(output_dir, exist_ok=True)
            
            filename = f"{self.name.replace(' ', '_')}.csv"
            filepath = os.path.join(output_dir, filename)
            
            pd.DataFrame(results).to_csv(filepath, index=False)
            print(f"Saved scraped data to {filepath}")
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}")
        except Exception as e:
            raise Exception(f"Scraping failed: {e}")