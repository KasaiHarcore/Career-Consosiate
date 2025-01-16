"""
The main driver.
"""

from os.path import abspath

from app.model import common
from app.model.register import register_all_models

from app.utils import util
from app.utils.reader import ResumeReader
from app.utils.parse import parse_resumes
from app.client import *
from app import log, globals

import os
import argparse
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

# Taking data
if __name__ == "__main__":
    log.print_banner("""Welcome to the C&C, this is a debug console for AI in HR.""")
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description = "Resume Parsing")
    parser.add_argument(
        "--folder",
        type = str,
        default = globals.default_working_folder,
        help = "The folder containing resumes to parse.",
    )
    
    parser.add_argument(
        "--job_description",
        type = str,
        default = globals.job_description,
        help = "The job description to compare the resumes against.",
    )
    
    parser.add_argument(
        "--custom_prompt",
        type = str,
        help = "The custom prompt to use for the scoring system.",
    )
    args = parser.parse_args()

    # Get the absolute path of the folder
    folder_path = abspath(args.folder)

    # Check if the folder exists
    if not os.path.exists(folder_path):
        log.print_error(f"Folder '{folder_path}' not found.")
        exit(1)

    # Initialize the ResumeReader
    log.print_output("Initializing resume reader...")
    reader = ResumeReader(folder_path)

    # Get the dataframes
    log.print_output("Reading resumes...")
    data = reader.get_pdf_dataframe()

    # Register all models
    register_all_models()

    # Set the desired model
    common.set_model('openrouter/meta-llama/llama-3.1-70b-instruct:free')

    # Parsing process
    log.print_output("Parsing resumes...")
    parse_resumes(folder_path, data, args.job_description, args.custom_prompt)
            
    # Save the data
    if len(globals.failed) > 0:
        with open("./data/failed.txt", "w", encoding = "utf-8") as f:
            for item in globals.failed:
                f.write(str(item) + "\n")
            print("Failed resumes saved in failed.txt")
            
    log.print_output("Saving data...")
        
    results_path = os.path.join(folder_path, "Results.csv")
    if os.path.exists(results_path):
        old_df = pd.read_csv(results_path)
        final_df = pd.concat([old_df, data], ignore_index=True)
        final_df.drop_duplicates(subset=["File"], keep="first", inplace=True)
    else:
        final_df = data
    final_df.to_csv(results_path, index=False)
    
    log.print_output("Data saved at Results.csv")
    
    log.print_banner("Process completed.")
            
    # Chat Section
    log.print_banner("Starting client...")

    app.launch(debug = True)
        

    
    
    