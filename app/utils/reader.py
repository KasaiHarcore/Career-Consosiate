import os
import shutil
from datetime import datetime
import pandas as pd
import pymupdf4llm as fitz

class ResumeReader:
    """
    The ResumeReader class is designed to automate the processing and extraction of data from resume files in both PDF and image formats.
    The class leverages various libraries such as pymupdf4llm for text extraction from PDFs and pytesseract for optical character recognition (OCR) on image files. 
    It supports categorizing and organizing resumes into a structured format for further analysis or processing. Key features include:
    
    - File Processing: It scans a given folder path to identify and process resume files in PDF (.pdf, .docx) and image formats (.jpg, .png).
    
    - PDF and Image Handling: PDF files are converted to markdown format for easy text extraction, while image files undergo OCR to extract text content using pytesseract.

    - Data Management: Extracted text from resumes is stored in two separate lists (pdf_data and image_data), which can be easily converted into Pandas DataFrames for further manipulation or analysis.

    - Data Retrieval: Provides methods to retrieve structured data as Pandas DataFrames for PDFs, images, or a combined set of both. These DataFrames can be used for further data analysis, categorization, or machine learning purposes.

    - File Organization: Includes a method to move files into categorized subfolders based on the extracted or predicted categories, allowing for easy organization of processed resumes.
    """
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.pdf_data = []  # To store resume data
        
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
                    self._process_text(resume_id, file_path)
                    resume_id += 1
        
            if resume_id == 1:
                print("No resumes found in the given folder path.")
                break

    def _process_text(self, resume_id, file_path):
        """Process the PDF file and extract content using pymupdf4llm."""
        try:
            context_reader = fitz.to_markdown(file_path)
            # ctg = model.predict(resume_content)
            
            # Append data to the PDF data list
            self.pdf_data.append({
                'ID': resume_id,
                'File': os.path.basename(file_path),
                'Resume': context_reader,
                'Category': 'Unknown', # Model prediction or manual categorization
                'Date_Processed': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            # self.move_file_to_category_folder(f'/PDF/{ctg}', file_path)
        except Exception as e:
            print(f"Error processing PDF {file_path}: {e}")
    
    def get_pdf_dataframe(self):
        """Return dataframe for PDF resumes."""
        return pd.DataFrame(self.pdf_data)
    
    def move_file_to_category_folder(category, file_path):
        """Move the file to the corresponding category folder."""
        base_folder = os.path.dirname(file_path)
        new_folder = os.path.join(base_folder, category)
        os.makedirs(new_folder, exist_ok = True)
        shutil.move(file_path, os.path.join(new_folder, os.path.basename(file_path)))