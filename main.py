"""
The main driver.
"""

import os
import argparse
from collections.abc import Callable, Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor
from itertools import chain
from os.path import abspath
from os.path import join as pjoin

from loguru import logger

from app import log, globals
from app.model import common
from app.model.register import register_all_models

from app import util
from app.utils.reader import ResumeReader
from app.utils.cleaner import ResumeCleaner

job_description_hr = """
Plan and implement talent attraction activities;
Recruit the right person, right job, right time;
Build and develop potential candidate data to ensure quality human resources for the company in the present and future;
Implement communications to bring Amigo's recruitment brand closer to candidates;
Organize recruitment programs in conjunction with IT training units.
Candidate requirements
Graduate from College/University;
At least 3 years of experience in recruiting in the IT field;
Proficient in using social networks, recruitment websites, managing candidate data and having a wide network of candidate relationships;
Experience working with universities to recruit Internships. Understanding the IT human resources market is an advantage;
Quick, flexible, quick to grasp problems;
Eager to learn, diligent, honest;
Good communication skills.
Benefits
Becoming an AMIGO member, you are not only guaranteed full social insurance, health insurance, unemployment insurance, vacation days, and holidays, but also enjoy competitive income and treatment policies in the market, working in a professional environment with young, enthusiastic colleagues who are always united, loving and sharing so that every working day is a happy day because of dedication and development.

Monthly income: Monthly salary + KPI bonus (20% of monthly salary)
Income package up to 17 months/year. Commitment to 13th month salary and year-end business results bonus.
Periodic reward activities (month/quarter/program/special achievements) such as: "Man of the month", "Creative star", Outstanding employee/team/department/division; Bonuses for completing training courses/professional certificates... according to company regulations
Comprehensive annual health insurance
Bonuses for holidays, Tet, birthdays...
Annual vacation/Innovation/Teambuilding regime
Periodic health check-up package up to 2,500,000 VND/person/year
Career development orientation with professional training programs and support for international certification exams.
Working location
- Hanoi: Room 501, 5th floor, Indochina Plaza Hanoi building, 241 Xuan Thuy, Cau Giay
Working hours
Monday - Friday (from 08:00 to 17:00)
"""

# Taking data
if __name__ == "__main__":
    # Set up logging
    log.setup_logging()

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description = "Resume Parsing")
    parser.add_argument(
        "--folder",
        type = str,
        default = "resumes",
        help = "The folder containing resumes to parse.",
    )
    args = parser.parse_args()

    # Get the absolute path of the folder
    if not os.path.isabs(args.folder):
        folder_path = abspath(args.folder)
    else:
        folder_path = globals.default_working_folder
        log.print_output(f"Using default folder '{folder_path}'.")

    # Check if the folder exists
    if not os.path.exists(folder_path):
        logger.error(f"Folder '{folder_path}' not found.")
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
    common.set_model("groq/llama-3.1-70b-versatile")

    log.print_llm("Parsing resumes...")
    for i in range(len(data)):
        prompt = data["resume"][i]
        log.print_with_time(f"Processing resume {i}...")
        messages = [
            {
                "role": "user",
                "content": 
                """Extract all JSON-like structures from the following unstructured text. The JSON structures may be inside curly braces `{...}` or square brackets `[...]`. Please return them as separate JSON objects or arrays. Text: """
                + 
                """<context>"""
                +
                prompt
                +
                """</context>"""
                +
                """Expected Output:
                1. Your JSON script return must be English.
                2. Extract all valid JSON-like structures.
                3. Follow the Output Format provided do not given anything else.
                4. Some information can be missing or incomplete, do not add any additional information.
                5. Leave the field empty if information is not present.

                Output format:
                ```json
                {
                        "Education": [
                            "University": ["..."], // Name of the university
                            "GPA": int, // average GPA
                            "Degree": ["..."] // optional
                        ],
                        "Experience": [
                                "Job Title": ["..."],
                                "Company": ["..."],
                                "Duration": int,  // sum up and convert to years
                                "Project": ["..."]
                        ],
                        "Skills": [
                            "...",
                            "..."
                            // Add more skills as needed (include both hard and soft skills)
                        ],
                }
                ```
                """
            }
        ]

        try:
            # Call the model
            response_content, cost, input_tokens, output_tokens = common.SELECTED_MODEL.call(
                messages = messages,
                response_format = "json_object",
                chat_mode = False
            )

            # Extract the JSON script
            json_script = util.extract_json(response_content['choices'][0]['message']['content'])
            parsed_data = util.data_filter(json_script)
            data['Education'][i] = parsed_data['Education']
            data['Experience'][i] = parsed_data['Experience']
            data['Skills'][i] = parsed_data['Skills']
            
        except Exception as e:
            logger.error(f"Error processing resume {i}: {e}")
            globals.failed.append(i)
            continue
    log.print_llm("Finished parsing resumes.")
        
    # Clean the data
    log.print_output("Cleaning data...")
    cleaner = ResumeCleaner(data)
    
    final_data = cleaner.get_data()
    
    
