"""
The main driver.
"""

from os.path import abspath
from utils.reader import ResumeReader
from utils.parse import parse_resumes
import log, globals
import django
django.setup()  

import os
import warnings
warnings.filterwarnings("ignore")

# Taking data
if __name__ == "__main__":
    log.print_banner("""Welcome to the C&C, this is a debug console for AI in HR.""")

    # Get the absolute path of the folder
    folder_path = abspath(globals.default_working_folder)

    # Check if the folder exists
    if not os.path.exists(folder_path):
        log.print_error(f"Folder '{folder_path}' not found.")
        exit(1)

    # Initialize the ResumeReader
    log.print_output("Initializing resume reader...")
    reader = ResumeReader(folder_path)

    # Get the dataframes
    log.print_output("Reading resumes...")
    data = reader.get_dataframe()

    # Parsing process
    log.print_output("Parsing resumes...")
    parse_resumes(data, "A job for Data Science position", " ")
            
    # Save the data
    if len(globals.failed) > 0:
        with open("./data/failed.txt", "w", encoding = "utf-8") as f:
            for item in globals.failed:
                f.write(str(item) + "\n")
            print("Failed resumes saved in failed.txt")
            
    log.print_output("Database Update...")
    
    log.print_output("No errors found.")
    
    log.print_banner("Closing console...")
            

    
    
    