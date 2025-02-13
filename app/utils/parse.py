import os
import datetime
import pandas as pd
import log
import globals

from utils import util, parse
from model import common
from model.register import register_all_models
from base.models import ResumeStorage

# Register AI models
register_all_models()
common.set_model('openrouter/meta-llama/llama-3.1-70b-instruct:free')  # AI model

def parse_resumes(data: pd.DataFrame, job_description: str, custom_prompt: str) -> bool:
    """
    Parses and processes resumes by calling an AI model for scoring and extracting details.

    Args:
        data (pd.DataFrame): DataFrame containing resume file paths and extracted text.
        job_description (str): The job description to compare against resumes.
        custom_prompt (str): Custom prompt to refine the AI model's response.

    Returns:
        bool: Returns True when processing is completed.
    """
    # Validate DataFrame
    if data.empty:
        log.print_error("Error: No resume data found to process.")
        return False

    log.print_with_time(f"Processing {len(data)} resumes...")

    # Iterate over DataFrame rows using .iterrows()
    for index, row in data.iterrows():
        try:
            # Extract resume file path and text from DataFrame row
            file_path = row['File']
            file_name = os.path.basename(file_path)
            resume_text = row['Resume']

            log.print_with_time(f"Processing resume {index + 1}/{len(data)}: {file_name}")

            # Construct prompt for AI model
            model_prompt = (
                globals.scoring_system_prompt +
                "\nUSER: " + custom_prompt +
                globals.return_format_prompt +
                "\nCONTENT: \nHere is the resume:\n" + resume_text +
                "\n\nHere is the job description:\n" + job_description
            )

            # Call AI model for processing
            response_content, cost, input_tokens, output_tokens = common.SELECTED_MODEL.call(
                response_format="text",
                messages=[{"role": "user", "content": model_prompt}]
            )

            # Log AI model details
            log.print_llm(f"Cost: {cost}, Input Tokens: {input_tokens}, Output Tokens: {output_tokens}")
            log.print_llm(f"Model Response: {response_content}")

            # Parse model response safely
            response_data = util.data_filter(response_content)

            # Store resume details in the database
            ResumeStorage.objects.create(
                resume_name="Manually added",
                resume_email=row['Email'],
                resume_phone=row['Phone'],
                resume_path=file_path,
                resume_text=resume_text,
                resume_date_added=datetime.datetime.now(),
                resume_education=response_data.get("Education", ""),
                resume_experience=response_data.get("Experience", 0.0),
                resume_tech_skills=response_data.get("Technical Skills", ""),
                resume_soft_skills=response_data.get("Soft Skills", ""),
                resume_certificates=response_data.get("Certificates", ""),
                resume_summary=response_data.get("Summary Comment", ""),
                resume_score=response_data.get("Score", 0.0),
                resume_AI_explanation=response_data.get("Explanation", "")
            )

        except KeyError as ke:
            log.print_error(f"KeyError in response parsing for resume {index + 1}: Missing key {ke}")
            globals.failed.append(file_name)

        except Exception as e:
            log.print_error(f"Unexpected error while processing resume {index + 1}: {e}")
            globals.failed.append(file_name)

    log.print_with_time("Resume processing completed.")
    return True
