
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
    product_sizes = []
    product_colors = []
    product_images = []
    if 'options' in product_data and 'productOptions' in product_data['options']:
        for option in product_data['options']['productOptions']:
            if option['label'] == 'size':
                product_sizes = [size['name'] for size in option['values']]
            elif option['label'] == 'color':
                product_colors = [color['name'] for color in option['values']]

    if 'media' in product_data:
      media_data = product_data['media']
      if 'main' in media_data and 'dynamic' in media_data['main']:
          main_image_url = media_data['main']['dynamic'].get('url', '')
          if main_image_url:
              product_images.append(f"https:{main_image_url}")
      if 'alternate' in media_data:
          for alternate_view in media_data['alternate'].values():
              if 'dynamic' in alternate_view:
                  alternate_image_url = alternate_view['dynamic'].get('url', '')
                  if alternate_image_url:
                      product_images.append(f"https:{alternate_image_url}")

    if not product_sizes:
        product_sizes = ["-"]
    if not product_colors:
        product_colors = ["-"]
    if not product_images:
        product_images = ["-"]

    product_skus_detail = product_data.get('skus', [])
    product_skus_data = []
    if 'skus' in product_data:
        product_skus_detail = product_data['skus']
        for sku in product_skus_detail:
            sku_name = sku.get('id', '')
            sku__color = sku.get('color', {}).get('name', '')
            sku_size = sku.get('size', {}).get('name', '')
            sku_stock = sku.get('stockStatusMessage')
            sku_stock_count = sku.get('stockLevel')
            sku_media = sku.get('media', {}).get('main', {}).get('dynamic', {}).get('url', '')
            product_skus_data.append({
                "ID": sku_name,
                "Status": sku_stock,
                "Color": sku__color,
                "Size": sku_size,
                "Image URL": f"https:{sku_media}",
                "Stock": sku_stock_count
            })

    extracted_product_data = {
        "ID": product_id,
        "Category": product_category,
        "Name": product_name,
        "Brand": product_brand,
        "Description": product_description,
        "Price": f"{product_currency} {product_price}",
        "Sizes": product_sizes,
        "Colors": product_colors,
        "Images": product_images,
        "URL": url,
        "Skus": product_skus_data
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
        if 'skus' in product_info:
            product_skus_detail = product_info['skus']
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
                    "Image URL": "-",
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
            "Images": product_colors_images,
            "Skus": product_skus_data
        })

    return extracted_product_details