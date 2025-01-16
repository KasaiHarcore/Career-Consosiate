import re
import json

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
        job_title = json_data.get("job_category", "")
        education = json_data.get("education_degree", [])
        experience = json_data.get("experience", 0)
        hskills = json_data.get("hard_skill", [])
        certificates = json_data.get("certificates", [])
        sskill = json_data.get("soft_skill", [])
        summary = json_data.get("summary_cv", "")
        score = json_data.get("fit_score", 0.0)
        explanation = json_data.get("explanation", "")

        result = {
            'Category': job_title,
            'Education': education,
            'Experience': experience,
            'Technical Skills': hskills,
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
            'Category': "",
            'Education': [],
            'Experience': 0,
            'Technical Skills': [],
            'Certificates': [],
            'Soft Skills': [],
            'Summary Comment': "",
            'Score': 0.0,
            'Explanation': "",
        }