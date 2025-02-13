import os
import re
import pandas as pd
from pdf2image import convert_from_path
import pytesseract
import textract
from PIL import Image

from utils import util
# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'.\utils\Tesseract-OCT\tesseract.exe'  # Path to Tesseract-OCR

import log
from base.models import ResumeStorage



class ResumeReader():
    """
    The ResumeReader class processes and extracts resume data from various file formats.
    Supports: PDF, DOCX, PNG, JPG, TIFF, BMP, GIF.
    """

    def __init__(self, input_path: str):
        self.resumes_data = []
        self.existing_files = set()

        # Determine input type (folder, list of files, single file)
        if isinstance(input_path, str) and os.path.isdir(input_path):
            self.files = self._get_files_from_folder(input_path)
        elif isinstance(input_path, list):
            self.files = [os.path.abspath(f) for f in input_path if os.path.isfile(f)]
        elif isinstance(input_path, str) and os.path.isfile(input_path):
            self.files = [os.path.abspath(input_path)]
        else:
            raise ValueError("Invalid input path. Must be a folder, list of file paths, or a single file path.")

        self.process_files()
        
    def _get_files_from_folder(self, folder_path):
        """Retrieve all valid resume files from the given folder."""
        valid_extensions = ('.pdf', '.docx', '.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')
        files = []
        for root, _, filenames in os.walk(folder_path):
            for file in filenames:
                if file.lower().endswith(valid_extensions):
                    files.append(os.path.join(root, file))
        if len(files) == 0:
            log.print_error(f"No valid resume files found in the input folder: {folder_path}")
        
        return files
    
    def process_files(self):
        """Process each file based on its format (PDF, DOCX, Images)."""
        for file_path in self.files:
            # Check for duplicate files in the database
            if ResumeStorage.objects.filter(resume_path=file_path).exists():
                log.print_output(f"Skipping existing file: {os.path.basename(file_path)}")
                continue
            
            file_ext = os.path.splitext(file_path)[1].lower()
            resume_content = ""

            if file_ext == ".pdf":
                resume_content = self._process_pdf(file_path)
            elif file_ext == ".docx":
                resume_content = self._process_docx(file_path)
            elif file_ext in [".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif"]:
                resume_content = self._process_image(file_path)
            else:
                log.print_error(f"Unsupported file format: {file_path}")
                continue  # Skip unsupported files

            # Extract personal information and encrypt email/phone
            extracted_info, encrypt_text = self.extract_candidate_info(resume_content)
            

            # Append extracted data
            self.resumes_data.append({
                'File': os.path.abspath(file_path),
                'Resume': encrypt_text,
                'Email': extracted_info['email'],
                'Phone': extracted_info['phone'],
            })

    def _process_pdf(self, file_path: str, config=''):
        """Process PDF files by converting them to images and extracting text using OCR."""
        try:
            images = convert_from_path(file_path, dpi=500, poppler_path=r'.\\utils\\poppler-24.08.0\\Library\\bin')

            resume_content = ''
            for i, image in enumerate(images):
                page_text = pytesseract.image_to_string(image, lang='eng+vie', config=config)
                resume_content += f"\n=== Page {i + 1} ===\n{page_text}"

            log.print_output(f"Successfully processed PDF: {file_path}")
            return resume_content

        except Exception as e:
            log.print_error(f"Error processing PDF {file_path}: {e}")
            return ""

    def _process_docx(self, file_path: str):
        """Process DOCX files by extracting plain text."""
        try:
            doc = textract.process(file_path)
            resume_content = doc.decode('utf-8')

            log.print_output(f"Successfully processed DOCX: {file_path}")
            return resume_content

        except Exception as e:
            log.print_error(f"Error processing DOCX {file_path}: {e}")
            return ""

    def _process_image(self, file_path: str, config=''):
        """Process image files (JPG, PNG, TIFF, etc.) by extracting text using OCR."""
        try:
            image = Image.open(file_path)
            resume_content = pytesseract.image_to_string(image, lang='eng+vie', config=config)

            log.print_output(f"Successfully processed Image: {file_path}")
            return resume_content

        except Exception as e:
            log.print_error(f"Error processing Image {file_path}: {e}")
            return ""

    def extract_candidate_info(self, resume_text: str):
        """
        Extracts candidate's name, email, and phone number.
        - Keeps the name unchanged.
        - Encrypts email & phone using AES.
        - Replaces original email/phone with their encrypted versions in the resume text.
    
        Args:
            resume_text (str): Extracted text from a resume.
    
        Returns:
            tuple: Dictionary containing 'email', 'phone' and updated 'resume_text'.
        """
    
        # Regular Expression Patterns
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        vietnamese_phone_pattern = r"\b0[1-9]{1}[0-9]{8}\b"  # Ensures 10-digit format
    
        # Extract Email & Phone
        email_match = re.search(email_pattern, resume_text)
        phone_match = re.search(vietnamese_phone_pattern, resume_text)
    
        email_encrypted = util.encrypt_CV(email_match.group()) if email_match else ""
        phone_encrypted = util.encrypt_CV(phone_match.group()) if phone_match else ""
    
        # Replace original email & phone in the resume text with encrypted versions
        if email_match:
            resume_text = resume_text.replace(email_match.group(), email_encrypted)
        if phone_match:
            resume_text = resume_text.replace(phone_match.group(), phone_encrypted)
    
        # Return email and phone and updated resume text
        return {"email": email_match.group() if email_match else "No email found",
                "phone": phone_match.group() if phone_match else "No phone number found"}, resume_text


    def get_dataframe(self):
        """Return a pandas DataFrame containing all extracted resume data."""
        return pd.DataFrame(self.resumes_data)
