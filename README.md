# Neiman Marcus Product Scraper

This project is a web scraper that extracts product data from the Neiman Marcus website. It retrieves information such as product name, category, brand, description, price, color, image URL, and SKU details.

## Features

- Scrapes product URLs from category pages
- Extracts detailed product information from individual product pages
- Saves scraped data in JSON format
- Implements caching to reduce unnecessary HTTP requests
- Uses concurrent programming with threading for faster scraping
- Includes logging for better visibility and debugging

## Create environment

```
python -m venv env
```
- Activate the virtual environment:
    - On Windows:
    ```
    env\Scripts\activate
    ```
    - On Unix or macOS:
    ```
    source env/bin/activate
    ```

## Install the required dependencies:
```
pip install -r requirements.txt
```

## Usage
1. Open the `main.py` file and modify the `url` variable with the desired category URL from the Neiman Marcus website.

2. Run the scraper:
```
python main.py
```

The scraper will start scraping the product URLs from the specified category page and then extract detailed information from each product page. The scraped data will be saved in a JSON file within the `data` folder, named after the category URL.

## Project Structure

- `main.py`: The main script that runs the scraper.
- `src/scraper.py`: Contains the `NeimanMarcusScraper` class for scraping product URLs.
- `src/item_extract.py`: Includes functions for extracting product data from the scraped HTML/JSON.
- `src/utils.py`: Utility functions for data cleaning and JSON file handling.
- `data/`: Directory where the scraped data is saved in JSON format.