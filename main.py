import json
import re
import logging
import random
import requests
from bs4 import BeautifulSoup
from src.scraper import NeimanMarcusScraper
from src.utils import json_data, setup_logging
from src.item_extract import extract_product_data
import threading
from time import sleep

setup_logging()

class MainScraper:
    """
    A class for scraping product data from the Neiman Marcus website.
    """

    def __init__(self):
        self.url_scraper = NeimanMarcusScraper()
        self.base_url = "https://www.neimanmarcus.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # To store scraped data temporarily
        self.cache = {}  

    @staticmethod
    def clean_url(url):
        """
        Removes query parameters from the given URL.

        Args:
            url (str): The URL to be cleaned.

        Returns:
            str: The cleaned URL without query parameters.
        """
        return re.sub(r'\?.*', '', url)

    def scrape_product_page(self, url):
        """
        Scrapes product data from a given product page URL.

        Args:
            url (str): The URL of the product page.

        Returns:
            list: A list of dictionaries containing the scraped product data.
        """
        cleaned_url = self.clean_url(url)
        if cleaned_url in self.cache:
            logging.info(f"Using cached data for {cleaned_url}")
            return self.cache[cleaned_url]

        try:
            response = requests.get(cleaned_url, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.error(f"Error accessing URL {cleaned_url}: {e}")
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        script_tag = soup.find('script', {'type': 'application/json'})
        if script_tag:
            script_content = script_tag.string.strip()
            data = json.loads(script_content)
            product_data = extract_product_data(data, cleaned_url)
            self.cache[cleaned_url] = product_data
            return product_data
        else:
            logging.warning("Product data not found.")
            return []

    def main(self, url):
        """
        Main function to scrape product data from the given URL.

        Args:
            url (str): The URL of the category page.
        """
        product_urls = self.url_scraper.scrape_all_product_urls(url)
        file_name = re.sub(r'[\?/]', '_', url.split('/')[-1])
        all_data = []

        # Using threading for parallel scraping
        threads = []
        for product_url in product_urls:
            thread = threading.Thread(target=self.scrape_and_append, args=(product_url, all_data))
            threads.append(thread)
            thread.start()
            
            # Random delay to avoid rate limiting
            sleep(random.uniform(0.5, 1))

        for thread in threads:
            thread.join()

        json_data(all_data, f"{file_name}.json", 'data')

    def scrape_and_append(self, url, data_list):
        """
        Scrapes product data from a given URL and appends it to a list.

        Args:
            url (str): The URL of the product page.
            data_list (list): The list to append the scraped data.
        """
        product_data = self.scrape_product_page(url)
        data_list.extend(product_data)

if __name__ == "__main__":
    with open("url_category.txt", "r", encoding="utf8") as file:
        url_category = file.read()
        
    url_category = url_category.split()
    for url in url_category:
        print("Processing: ", url)
        main_scraper = MainScraper()
        main_scraper.main(url)