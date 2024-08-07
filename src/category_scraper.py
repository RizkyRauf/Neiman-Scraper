import requests
import xml.etree.ElementTree as ET
import json
import gzip
from io import BytesIO
from src.utils import json_category

class CategoryScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
        }
        self.namespaces = {
            'sit': 'http://www.sitemaps.org/schemas/sitemap/0.9',
            'image': 'http://www.google.com/schemas/sitemap-image/1.1',
            'xhtml': 'http://www.w3.org/1999/xhtml',
            'video': 'http://www.google.com/schemas/sitemap-video/1.1'
        }

    def get_xml_content(self, url):
        response = requests.get(url, headers=self.headers)
        if response.headers.get('Content-Encoding') == 'gzip':
            compressed_file = BytesIO(response.content)
            with gzip.open(compressed_file, 'rb') as f:
                return f.read()
        return response.content

    def parse_xml(self, xml_content):
        root = ET.fromstring(xml_content)
        data = []
        for url in root.findall('sit:url', self.namespaces):
            loc = url.find('sit:loc', self.namespaces).text
            lastmod = url.find('sit:lastmod', self.namespaces)
            lastmod = lastmod.text if lastmod is not None else None
            data.append({
                "URL": loc,
                "LastModified": lastmod
            })
        return data

    def get_categories(self):
        url_sitemap = ["https://www.neimanmarcus.com/sitemap_category_1.xml.gz"]
        all_data = []

        for url in url_sitemap:
            xml_content = self.get_xml_content(url)
            data = self.parse_xml(xml_content)
            all_data.extend(data)

        json_category(all_data, 'category.json', 'data')
        return json.dumps(all_data)