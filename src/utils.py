import os
import re
import logging
import json

def json_category(data_list, filename, folder_path) -> None:
    """
    Saves a list of dictionaries to a JSON file, combining with existing data if the file already exists.
    Removes duplicate dictionaries based on their string representation.

    Args:
        data_list (list): A list of dictionaries to be saved.
        filename (str): The name of the JSON file.
        folder_path (str): The path to the folder where the JSON file will be saved.

    Returns:
        None
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, filename)

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    combined_data = existing_data + data_list

    unique_data = list({json.dumps(data_dict, sort_keys=True) for data_dict in combined_data})
    unique_data = [json.loads(data_str) for data_str in unique_data]

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(unique_data, file, ensure_ascii=False, indent=4)

    print(f'Data saved to {file_path}')

def json_data(data_list, filename, folder_path) -> None:
    """
    Saves a list of dictionaries to a JSON file, combining with existing data if the file already exists.
    Removes duplicate dictionaries based on their string representation.

    Args:
        data_list (list): A list of dictionaries to be saved.
        filename (str): The name of the JSON file.
        folder_path (str): The path to the folder where the JSON file will be saved.

    Returns:
        None
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, filename)

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    combined_data = existing_data + data_list

    unique_data = list({json.dumps(data_dict, sort_keys=True) for data_dict in combined_data})
    unique_data = [json.loads(data_str) for data_str in unique_data]

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(unique_data, file, ensure_ascii=False, indent=4)

    print(f'Data saved to {file_path}')

def clean_description(description_text):
    """
    Cleans and formats a given description text.

    Args:
        description_text (str): The description text to be cleaned.

    Returns:
        str: The cleaned and formatted description text.
    """
    if description_text:
        description_text = re.sub(r'<[^>]+>', '', description_text)
        description_text = re.sub(r'\s+', ' ', description_text)
        description_text = description_text.strip()
        description_text = description_text.replace(',', '.')
        description_text = description_text.replace('���', '���')
    return description_text

def setup_logging(log_level=logging.INFO, log_format='%(asctime)s - %(levelname)s - %(message)s'):
    """
    Sets up the logging configuration to log to a file.

    Args:
        log_level (int, optional): The logging level. Defaults to logging.INFO.
        log_format (str, optional): The logging format. Defaults to '%(asctime)s - %(levelname)s - %(message)s'.
    """
    log_dir = 'logging'
    log_file = 'app.log'
    log_path = os.path.join(log_dir, log_file)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ]
    )