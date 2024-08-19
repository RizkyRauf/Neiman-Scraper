import json
import re
import logging
import aiohttp
import asyncio
import lxml.html
from multiprocessing import Pool
from itertools import chain
import diskcache
from src.scraper import NeimanMarcusScraper
from src.utils import json_data, setup_logging
from src.item_extract import extract_product_data

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
        self.cache = diskcache.Cache("./cache")

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

    async def scrape_product_page(self, url):
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
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers) as response:
                    response.raise_for_status()
                    html = await response.text()
        except aiohttp.ClientError as e:
            logging.error(f"Error accessing URL {cleaned_url}: {e}")
            return []

        tree = lxml.html.fromstring(html)
        script_tag = tree.xpath('//script[@type="application/json"]/text()')
        if script_tag:
            script_content = script_tag[0].strip()
            data = json.loads(script_content)
            product_data = extract_product_data(data, cleaned_url)
            self.cache[cleaned_url] = product_data
            return product_data
        else:
            logging.warning("Product data not found.")
            return []

    async def main(self, url):
        """
        Main function to scrape product data from the given URL.

        Args:
            url (str): The URL of the category page.
        """
        product_urls = self.url_scraper.scrape_all_product_urls(url)
        file_name = re.sub(r'[\?/]', '_', url.split('/')[-1])
        tasks = [self.scrape_product_page(url) for url in product_urls]
        all_data = await asyncio.gather(*tasks)
        json_data(all_data, f"{file_name}.json", 'data')

    def scrape_and_append(self, url):
        product_data = asyncio.run(self.scrape_product_page(url))
        return product_data

if __name__ == "__main__":
    with open("url_category.txt", "r", encoding="utf8") as file:
        url_category = file.read().splitlines()

    for url in url_category:
        print("Processing: ", url)
        main_scraper = MainScraper()
        product_urls = main_scraper.url_scraper.scrape_all_product_urls(url)
        with Pool() as pool:
            product_data = pool.map(main_scraper.scrape_and_append, product_urls)
            all_data = list(chain(*product_data))

        # Filter out products with invalid or empty values
        valid_products = [product for product in all_data if product["Brand"] and product["Name"] and product["Price"] and product["ID"]]

        # Flatten the "Images" list
        for product in valid_products:
          product["Images"] = product["Images"]
          if "Skus" in product:
              product["Skus"] = [sku for sku in product["Skus"]]
          else:
              None

        # Save the cleaned data to a JSON file with the category URL as the filename
        file_name = re.sub(r'[\?/]', '_', url.split('/')[-1]) + ".json"
        json_data(valid_products, file_name, 'data')