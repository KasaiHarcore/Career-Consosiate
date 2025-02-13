import re
import json
import globals

import log
# Securely store and retrieve the secret key
from Crypto.Cipher import AES
import base64

def data_filter(output: str) -> dict:
    """
    Parses the JSON string and extracts relevant sections.

    Parameters:
    - output (str): The JSON data as a string.

    Returns:
    - dict: A dictionary containing parsed data for each section.
    """
    output_list = re.findall(r"```(.*?)```", output, re.DOTALL)
    if output_list:
        output = output_list[0]
    else:
        pass  # Handle this case as needed

    try:
        # Parse the JSON string
        json_data = json.loads(output.strip())

        # Extract sections with default empty structures if not present
        name = json_data.get("name", "")
        education = json_data.get("education_degree", [])
        experience = json_data.get("experience", 0.0)
        tskills = json_data.get("technicial_skill", [])
        certificates = json_data.get("certificates", [])
        sskill = json_data.get("soft_skill", [])
        summary = json_data.get("summary_cv", "")
        score = json_data.get("fit_score", 0.0)
        explanation = json_data.get("explanation", "")
        
        if len(summary) == 0:
            return False

        result = {
            'Name': name,
            'Education': education,
            'Experience': experience,
            'Technical Skills': tskills,
            'Certificates': certificates,
            'Soft Skills': sskill,
            'Summary Comment': summary,
            'Score': score,
            'Explanation': explanation,
        }
        return result

    except json.JSONDecodeError as e:
        # Handle JSON decoding errors
        print(f"Error decoding JSON: {e}")
        return {
            'Name': "",
            'Education': [],
            'Experience': 0.0,
            'Technical Skills': [],
            'Certificates': [],
            'Soft Skills': [],
            'Summary Comment': "",
            'Score': 0.0,
            'Explanation': "",
        }
        
def encrypt_CV(data):
    """Encrypts data using AES encryption (EAX mode) and includes nonce."""
    try:
        cipher = AES.new(globals.SECURITY_KEY, AES.MODE_EAX)
        nonce = cipher.nonce  # Generate unique nonce
        ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
        return base64.b64encode(nonce + ciphertext).decode('utf-8')
    except Exception as e:
        log.print_error(f"Encryption error: {e}")
        return ""

# Use if needed else skip this
def decrypt_CV(encrypted_data):
    """Decrypts AES-encrypted email or phone numbers securely."""
    try:
        encrypted_data = base64.b64decode(encrypted_data)
        if len(encrypted_data) < 16:
            raise ValueError("Invalid encrypted data: Missing nonce.")

        nonce = encrypted_data[:16]  # Extract nonce
        ciphertext = encrypted_data[16:]  # Extract ciphertext
        cipher = AES.new(globals.SECURITY_KEY, AES.MODE_EAX, nonce=nonce)

        return cipher.decrypt(ciphertext).decode('utf-8')

    except Exception as e:
        log.print_error(f"Decryption error: {e}")
        return ""  # Return empty string if decryption fails
