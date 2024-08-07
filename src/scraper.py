import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class NeimanMarcusScraper:
    """
    A class for scraping product URLs from the Neiman Marcus website.
    """

    def __init__(self):
        self.base_url = "https://www.neimanmarcus.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_product_urls(self, url):
        """
        Retrieves the product URLs and the URL for the next page from a given URL.

        Args:
            url (str): The URL to scrape.

        Returns:
            tuple: A tuple containing two elements:
                - A list of product URLs scraped from the given URL.
                - The URL for the next page, or None if there is no next page.
        """
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        product_url_elements = soup.find_all('div', class_='product-thumbnail')
        product_urls = [urljoin(self.base_url, link['href'])
                        for product_element in product_url_elements
                        if (link := product_element.find('a', class_='product-thumbnail__link')) and 'href' in link.attrs]

        next_page_element = soup.find('a', class_='arrow-button--right')
        next_page_url = urljoin(self.base_url, next_page_element['href']) if next_page_element else None

        return product_urls, next_page_url

    def scrape_all_product_urls(self, start_url):
        """
        Scrapes all product URLs from the given start URL and its subsequent pages.

        Args:
            start_url (str): The starting URL to begin scraping.

        Returns:
            list: A list of all product URLs scraped from the start URL and its subsequent pages.
        """
        all_product_urls = []
        current_url = start_url

        while current_url:
            print(f"Scraping: {current_url}")
            product_urls, current_url = self.get_product_urls(current_url)
            all_product_urls.extend(product_urls)

        return all_product_urls