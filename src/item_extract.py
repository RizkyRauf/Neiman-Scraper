
from src.utils import clean_description

def extract_product_data(data, url):
    """
    Extracts product data from the given data dictionary.

    Args:
        data (dict): The dictionary containing product data.
        url (str): The URL of the product page.

    Returns:
        list: A list of dictionaries containing extracted product data.
    """
    extracted_product_data = []
    if 'props' in data and 'pageProps' in data['props']:
        page_props = data['props']['pageProps']
        if 'productData' in page_props:
            extracted_product_data.append(extract_product_data_from_props(page_props['productData'], url))

    elif 'productCatalog' in data:
        extracted_product_data.extend(extract_product_data_from_catalog(data['productCatalog'], url))

    return extracted_product_data


def extract_product_data_from_props(product_data, url):
    """
    Extracts product data from the 'productData' dictionary.

    Args:
        product_data (dict): The 'productData' dictionary containing product information.
        url (str): The URL of the product page.

    Returns:
        dict: A dictionary containing extracted product data.
    """
    category_hierarchy = product_data.get('hierarchy', [])
    category_levels = []
    for category in category_hierarchy:
        category_levels.extend([value for value in category.values() if value])
    product_category = " > ".join(category_levels)
    product_id = product_data.get('id')
    product_brand = product_data.get('designer', {}).get('name', '')
    product_name = product_data.get('name')
    product_price = product_data.get('price', {}).get('retailPrice', '')
    product_currency = product_data.get('price', {}).get('currencyCode', '')
    product_description = clean_description(product_data.get('details', {}).get('longDesc', ''))
    product_image_url = product_data.get('media', {}).get('main', {}).get('dynamic', {}).get('url', '')
    product_options = product_data.get('options', {}).get('productOptions', [])
    product_colors = product_data.get('options', {}).get('productOptions', [])
    color_names = []
    for option in product_colors:
        if option.get('label', '').lower() == 'color':
            for color in option.get('values', []):
                color_names.append(color.get('name', ''))
    product_colors_str = ', '.join(color_names)

    product_skus_detail = product_data.get('skus', [])
    product_skus_data = []
    for sku in product_skus_detail:
        sku_id = sku.get('id')
        sku_status = sku.get('stockStatusMessage')
        sku_color = sku.get('color', {}).get('name', '')
        sku_stock_level = sku.get('stockLevel')
        product_skus_data.append({
            "ID": sku_id,
            "Status": sku_status,
            "Color": sku_color,
            "Stock": sku_stock_level
        })

    extracted_product_data = {
        "ID": product_id,
        "Category": product_category,
        "Name": product_name,
        "Brand": product_brand,
        "Description": product_description,
        "Price": f"{product_currency} {product_price}",
        "Color": product_colors_str,
        "Image URL": f"https:{product_image_url}",
        "URL": url,
        "SKU": product_skus_data
    }

    return extracted_product_data


def extract_product_data_from_catalog(product_data, url):
    """
    Extracts product data from the 'productCatalog' dictionary.

    Args:
        product_data (dict): The 'productCatalog' dictionary containing product information.
        url (str): The URL of the product page.

    Returns:
        list: A list of dictionaries containing extracted product data.
    """
    extracted_product_details = []
    if 'product' in product_data:
        category_hierarchy = product_data['product'].get('hierarchy', [])
        category_levels = []
        for category in category_hierarchy:
            category_levels.extend([value for value in category.values() if value])
        product_category = " > ".join(category_levels)
        product_id = product_data['product'].get('id', '')
        product_name = product_data['product'].get('linkedData', {}).get('name', '')
        product_brand = product_data['product'].get('linkedData', {}).get('brand', '')
        product_description = clean_description(product_data['product'].get('linkedData', {}).get('description', ''))
        product_image_url = product_data['product'].get('linkedData', {}).get('image', '')
        product_currency = product_data['product'].get('linkedData', {}).get('offers', {}).get('priceCurrency', '')
        product_low_price = product_data['product'].get('linkedData', {}).get('offers', {}).get('lowPrice', '')
        product_high_price = product_data['product'].get('linkedData', {}).get('offers', {}).get('highPrice', '')
        product_offers = product_data['product'].get('linkedData', {}).get('offers', {}).get('offers', [])
        product_colors = [offer.get('itemOffered', {}).get('color', '') for offer in product_offers if offer.get('itemOffered', {}).get('color', '')]
        product_colors_str = ", ".join(product_colors)

        product_skus_detail = product_data['product'].get('skus', [])
        product_skus_data = []
        for sku in product_skus_detail:
            sku_id = sku.get('id', '-')
            sku_status = sku.get('stockStatusMessage', '-')
            sku_color = sku.get('color', {}).get('name', '')
            sku_stock_level = sku.get('stockLevel', '-')
            product_skus_data.append({
                "ID": sku_id,
                "Status": sku_status,
                "Color": sku_color,
                "Stock Level": sku_stock_level
            })

        extracted_product_details.append({
            "ID": product_id,
            "Category": product_category,
            "Name": product_name,
            "Brand": product_brand,
            "Description": product_description,
            "Price": f"{product_currency} {product_low_price}",
            # "High Price": f"{product_currency} {product_high_price}",
            "Color": product_colors_str,
            "Image URL": product_image_url,
            "Url": url,
            "Skus": product_skus_data
        })

    return extracted_product_details