import log

from base.models import ResumeStorage
from ai_logics import build_ai_prompt, call_ai_model, parse_ai_response
from utils.util import parse_list_to_string, parse_float_safe
import globals

def parse_resumes(resume_ids: list, job_description: str, custom_prompt: str) -> bool:
    """
    Parses and processes resumes by calling an AI model for scoring and extracting details.

    Args:
        data: DataFrame containing resume file paths and extracted text.
        job_description: The job description to compare against resumes.
        custom_prompt: Custom prompt to refine the AI model's response.

    Returns:
        bool: Returns True when processing is completed.
    """
    resumes = ResumeStorage.objects.filter(resume_id__in = resume_ids)

    if not resumes.exists():
        log.print_error("No resumes found for processing.")
        return False

    log.print_with_time(f" Processing {len(resumes)} resumes...")

    for resume in resumes:
        try:
            log.print_with_time(f"Processing resume: {resume.resume_path}")


            model_prompt = build_ai_prompt(
                resume_text=resume.resume_text,
                job_description=job_description,
                custom_prompt=custom_prompt
            )

            response_content = call_ai_model(model_prompt)

            response_data = parse_ai_response(response_content)
            if not response_data:
                log.print_error(f"Error parsing resume {resume.resume_path}. Skipping.")
                globals.failed.append(resume.resume_path)
                continue

            resume.resume_education = parse_list_to_string(
                response_data.get("Education", resume.resume_education or "No Info")
            )
            resume.resume_experience = parse_float_safe(
                response_data.get("Experience", resume.resume_experience or 0.0)
            )
            resume.resume_tech_skills = parse_list_to_string(
                response_data.get("Technical Skills", resume.resume_tech_skills or "No Info")
            )
            resume.resume_soft_skills = parse_list_to_string(
                response_data.get("Soft Skills", resume.resume_soft_skills or "No Info")
            )
            resume.resume_certificates = parse_list_to_string(
                response_data.get("Certificates", resume.resume_certificates or "No Info")
            )
            resume.resume_summary = response_data.get(
                "Summary Comment", resume.resume_summary or "No Info"
            )
            resume.resume_score = parse_float_safe(
                response_data.get("Score", resume.resume_score or 0.0)
            )
            resume.resume_AI_explanation = response_data.get(
                "Explanation", resume.resume_AI_explanation or "No Info"
            )

            resume.save()

        except Exception as e:
            log.print_error(f"Error processing resume {resume.resume_path}: {e}")
            globals.failed.append(resume.resume_path)

    log.print_with_time("Completed processing resumes.")
    return True