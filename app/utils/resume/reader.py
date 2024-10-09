import os
import shutil
from PIL import Image
import numpy as np
import pandas as pd
import pymupdf4llm as fitz
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\\Game\\github\\Tesseract-OCR"


class ResumeReader:
    """
    Class to process resumes from a given folder path.
    
    Attributes:
    -----------
    folder_path: str
        Path to the folder containing resumes.
        
    pdf_data: list
        List to store PDF resume data.
        
    image_data: list
        List to store image resume data.
        
        
    Methods:
    --------
    process_files():
        Main method to process both PDF and image files.
        
    _process_text(file_path):
        Process the PDF file and extract content using pymupdf4llm.
        
    _process_image(file_path):
        Process image file and store the path.
        
    get_pdf_dataframe():
        Return dataframe for PDF resumes.
        
    get_image_dataframe():
        Return dataframe for images.
    
    get_all_resumes_dataframe():
        Return a combined dataframe for all resumes.
        
    move_file_to_category_folder(category, file_path):
        Move the file to the corresponding category folder.
    """
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.pdf_data = []  # To store resume data
        self.image_data = []  # To store image path data
        
        self.process_files()
        
    def _reset_data(self):
        """Reset the data lists."""
        self.pdf_data = []
        self.image_data = []

    def process_files(self):
        """Main method to process both PDF and image files."""
        resume_id = 1
        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Check for PDF files
                if file.endswith(('.pdf', '.docx')):
                    self._process_text(file_path)
                
                # Check for image files
                elif file.endswith(('.jpg', '.png')):
                    self._process_image(resume_id, file_path)
                    resume_id += 1
            if resume_id == 1:
                print("No resumes found in the given folder path.")
                break

    def _process_text(self, file_path):
        """Process the PDF file and extract content using pymupdf4llm."""
        try:
            context_reader = fitz.to_markdown(file_path)
            # ctg = model.predict(resume_content)
            
            # Append data to the PDF data list
            self.pdf_data.append({
                'resume': context_reader,
                'category': None # ML Model Predict (ctg) or manual input
            })
            
            # self.move_file_to_category_folder(f'/PDF/{ctg}', file_path)
        except Exception as e:
            print(f"Error processing PDF {file_path}: {e}")
            
    def _process_image(self, file_path, lang = 'eng', config = r'--oem 3 --psm 6'):
        """Process image file and store the path."""
        try:
            extracted_text = pytesseract.image_to_string(Image.open(file_path), lang = lang, config = config)
            self.image_data.append({
                'resume': extracted_text,
                'category': None # ML Model Predict
            })
            
            # self.move_file_to_category_folder(f'/PDF/{ctg}', file_path)
        except Exception as e:
            print(f"Error processing image {file_path}: {e}")
            print("Please check the image path or try changing the language or config.")
    
    def get_pdf_dataframe(self):
        """Return dataframe for PDF resumes."""
        return pd.DataFrame(self.pdf_data)

    def get_image_dataframe(self):
        """Return dataframe for images."""
        return pd.DataFrame(self.image_data)
    
    def get_all_resumes_dataframe(self):
        """Return a combined dataframe for all resumes."""
        pdf_df = pd.DataFrame(self.pdf_data)
        image_df = pd.DataFrame(self.image_data)
        return pd.concat([pdf_df, image_df], ignore_index = True)
    
    def move_file_to_category_folder(category, file_path):
        """Move the file to the corresponding category folder."""
        base_folder = os.path.dirname(file_path)
        new_folder = os.path.join(base_folder, category)
        os.makedirs(new_folder, exist_ok = True)
        shutil.move(file_path, os.path.join(new_folder, os.path.basename(file_path)))