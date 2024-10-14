import re
import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def extract_json(text: str) -> str:
    """
    Extracts the JSON script from the given text.
    """
    pattern = r'(?<=```json\n)(.*?)(?=```$)'
    match = re.search(pattern, text, re.DOTALL)
    json_script = match.group(0)
    return json_script + "]"


def data_filter(output: str) -> dict:
    """
    Parses the JSON string and extracts relevant sections.

    Parameters:
    - output (str): The JSON data as a string.

    Returns:
    - dict: A dictionary containing parsed data for each section.
    """
    try:
        # Parse the JSON string
        json_data = json.loads(output)
        
        # If the JSON data is a list, take the first element
        if isinstance(json_data, list):
            json_data = json_data[0]
        
        # Extract sections with default empty structures if not present
        education = json_data.get('Education', [])
        experience = json_data.get('Experience', [])
        skills = json_data.get('Skills', [])
        
        return {
            'Education': education,
            'Experience': experience,
            'Skills': skills,
        }
        
    except json.JSONDecodeError as e:
        print(f"JSON decoding failed: {e}")
        return {
            'Education': [],
            'Experience': [],
            'Skills': [],
        }
        
def get_tfidf_vectorizer(corpus: list[str]) -> TfidfVectorizer:
    """
    Returns a TfidfVectorizer object with the given corpus.

    Parameters:
    - corpus (list[str]): A list of strings to fit the vectorizer.

    Returns:
    - TfidfVectorizer: A TfidfVectorizer object fitted with the corpus.
    """
    vectorizer = TfidfVectorizer(stop_words = 'english')
    vectorizer.fit(corpus)
    return vectorizer

def get_cosine_similarity(matrix_1, matrix_2):
    """
    Calculate the cosine similarity between two matrices.

    Parameters:
    - matrix_1 (array-like): The first matrix.
    - matrix_2 (array-like): The second matrix.

    Returns:
    - array-like: The cosine similarity between the two matrices.
    """
    return cosine_similarity(matrix_1, matrix_2)