
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
    Mengekstrak data produk dari dictionary 'productCatalog'.

    Args:
        product_data (dict): Dictionary 'productCatalog' yang berisi informasi produk.
        url (str): URL halaman produk.

    Returns:
        list: Daftar dictionary yang berisi data produk yang diekstrak.
    """
    extracted_product_details = []

    if 'product' in product_data:
        product_info = product_data['product']

        # Mengekstrak kategori produk
        category_hierarchy = product_info.get('hierarchy', [])
        category_levels = []
        for category in category_hierarchy:
            category_levels.extend([value for value in category.values() if value])
        product_category = " > ".join(category_levels)

        # Mengekstrak informasi dasar produk
        product_id = product_info.get('id', '')
        product_name = product_info.get('linkedData', {}).get('name', '')
        product_brand = product_info.get('linkedData', {}).get('brand', '')
        product_description = clean_description(product_info.get('linkedData', {}).get('description', ''))
        product_currency = product_info.get('linkedData', {}).get('offers', {}).get('priceCurrency', '')
        product_low_price = product_info.get('linkedData', {}).get('offers', {}).get('lowPrice', '')
        product_high_price = product_info.get('linkedData', {}).get('offers', {}).get('highPrice', '')

        # Mengekstrak opsi produk (ukuran, warna, dan gambar)
        product_sizes = []
        product_colors_images = []
        product_options = product_info.get('options', {}).get('productOptions', [])
        for option in product_options:
            option_label = option.get('label', '').lower()
            if option_label == 'size':
                for size in option.get('values', []):
                    size_name = size.get('name', '-')
                    product_sizes.append(size_name)
            elif option_label == 'color':
                for color in option.get('values', []):
                    color_name = color.get('name', '-')
                    image_urls = []
                    main_image_url = color.get('media', {}).get('main', {}).get('dynamic', {}).get('url', '-')
                    image_urls.append(f"https:{main_image_url}")
                    image_alternate_url = color.get('media', {}).get('alternate', {})
                    for value in image_alternate_url.values():
                        alternate_image_url = value.get('dynamic', {}).get('url', '-')
                        image_urls.append(f"https:{alternate_image_url}")
                    product_colors_images.append({
                        "Color": color_name,
                        "Image URL": image_urls
                    })

        product_sizes_str = ', '.join(product_sizes) if product_sizes else '-'
        product_colors_str = ', '.join([color['Color'] for color in product_colors_images]) if product_colors_images else '-'

        # Mengekstrak detail SKU produk
        product_skus_detail = product_info.get('skus', [])
        product_skus_data = []
        for sku in product_skus_detail:
            sku_id = sku.get('id', '-')
            sku_status = sku.get('stockStatusMessage', '-')
            sku_color = sku.get('color', {}).get('name', '-')
            sku_stock_level = sku.get('stockLevel', '-')
            sku_size = sku.get('size', {}).get('name', '-')

            # Memberikan nilai default "-" jika tidak ada nilai
            sku_id = sku_id if sku_id != '-' else "-"
            sku_status = sku_status if sku_status != '-' else "-"
            sku_color = sku_color if sku_color != '-' else "-"
            sku_stock_level = str(sku_stock_level) if sku_stock_level != '-' else "-"
            sku_size = sku_size if sku_size != '-' else "-"

            product_skus_data.append({
                "ID": sku_id,
                "Status": sku_status,
                "Color": sku_color,
                "Size": sku_size,
                "Stock Level": sku_stock_level
            })

        extracted_product_details.append({
            "Url": url,
            "ID": product_id,
            "Category": product_category,
            "Name": product_name,
            "Brand": product_brand,
            "Description": product_description,
            "Price": f"{product_currency} {product_low_price}",
            "Size": product_sizes_str,
            "Color": product_colors_str,
            "Details Product Image URL": product_colors_images,
            "Skus": product_skus_data
        })

    return extracted_product_details