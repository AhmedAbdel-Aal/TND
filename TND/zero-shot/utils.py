import numpy as np
import json

def load_npy(file_path):
    """
    Load a .npy file and return its content as a NumPy array.

    Parameters:
        file_path (str): The path to the .npy file.

    Returns:
        numpy.ndarray: The content of the .npy file as a NumPy array.
    """
    try:
        data = np.load(file_path)
        return data
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except:
        print(f"An error occurred while loading '{file_path}'.")
        return None


def save_npy(data, file_path):
    """
    Save data as a .npy file.

    Parameters:
        data (numpy.ndarray): The data to be saved.
        file_path (str): The path where the .npy file will be saved.
    """
    try:
        np.save(file_path, data)
        print(f"Data successfully saved to '{file_path}'")
    except Exception as e:
        print(f"An error occurred while saving '{file_path}': {e}")

        
        
def load_json(path):
    # Open the JSON file
    with open(path, 'r') as f:
        # Load JSON data from file
        data = json.load(f)
    #print(f'data loaded from path {path}')
    return data


def save_json(data, path):
    """
    Save data as a JSON file.

    Parameters:
        data (dict): The dictionary to be saved as JSON.
        path (str): The path where the JSON file will be saved.
    """
    try:
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)
        #print(f"Data successfully saved to '{path}'")
    except Exception as e:
        print(f"An error occurred while saving '{path}': {e}")
        
        

def load_text_file(file_path):
    """
    Opens and reads the contents of a text file.
    
    :param file_path: The path to the text file.
    :return: The content of the file as a string.
    """
    try:
        # Open the file in read mode
        with open(file_path, 'r') as file:
            # Read the contents of the file
            content = file.read()
            return content
    except FileNotFoundError:
        print("Error: The file does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

        
        
def save_text_file(content, file_path):
    """
    Writes content to a text file.

    Parameters:
        content (str): The content to be written to the file.
        file_path (str): The path where the text file will be saved.
    """
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"File '{file_path}' successfully written.")
    except Exception as e:
        print(f"An error occurred while writing to '{file_path}': {e}")


def clean_text(text):
    return replace_unicode_with_space(text)

import re
def replace_unicode_with_space(text):
    # \u0000-\uFFFF matches all Unicode characters in the Basic Multilingual Plane (BMP)
    # This will replace every Unicode character with a space
    text =  re.sub(r'[^\x00-\x7F]', ' ', text)
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    # Strip leading and trailing spaces
    text = text.strip()

    return text


import re

def extract_special_format(text):
    """
    Detects and extracts any string in the form of dddd/dd from the given text.
    """
    # Define the regex pattern for dddd/dd
    pattern = r'\b\d{4}/\d{2}\b'
    # Find all matches in the text
    matches = re.findall(pattern, text)
    return matches


def flatten_elements(elements_list):
    
    content_list = []
    
    
    for element in elements_list:
        content_list.append(clean_text(element['content']))
        
        if len(element['elements']) > 0:
            content_list.append(flatten_elements(element['elements']))
    return '\n'.join(content_list)#content_list
 

def get_content(sections):
    r = {}
    for section in sections:
        content, elements = section['content'], section['elements']
        
        if 'section_name' not in section.keys():
            section_name = 'other'
        else:
            section_name = section['section_name']
        
        elements = flatten_elements(elements)
        
        
        if section_name not in r.keys(): 
            r[section_name] = elements
        else:
             r[section_name] =  r[section_name] + elements
    return r