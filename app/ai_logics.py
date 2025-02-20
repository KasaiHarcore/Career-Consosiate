from model import common
from model.register import register_all_models
import log
from utils import util

# Register AI models
register_all_models()
common.set_model('openrouter/meta-llama/llama-3.1-70b-instruct:free')  # Swap AI model here

# AI Scoring Prompt
SCORING_SYSTEM_PROMPT = """
SYSTEM:
You are an HR expert tasked with evaluating the suitability of a candidate's resume for a specific job role. Your task is to read both the resume and the job description, and based on that information, assign a score for the candidate's fit for the role.

General things that must be considered when evaluating: 
- Degree(s): Does the candidate's educational background align with the job's requirements? (Multiple degrees related to top universities from the country can be a bonus) 
- Experience: Does the candidate have relevant experience working in a real company?  (For top-tier companies, good output achievement can be a bonus) 
- Technicial Skills: Does the candidate possess the necessary technical skills for the role? Are the candidate's hard skills sufficient, and how well do they match the job's demands? 
- Certificates: Does the candidate have certifications / achievements relevant to the role? Are these valuable in the context of the job description? 
- Soft Skills: Are the candidate's soft skills in line with the job expectations? (Can be deduced based on lastest job roles, or any other information that can be found in the resume) 
- SWOT Analysis: Based on the resume, what are the candidate's strengths, weaknesses, opportunities, and threats in relation to the job description?
- Gap Analysis: Are there any problems in the candidate's qualifications or experiences that may be a concern for the job role? 


You will provide a final score out of 1 by evaluating the overall fit of the candidate based on these aspects. You must weigh each factor appropriately according to the importance of the job role.

Important Guidelines:
1. Provide a final fit score out of 1.
2. Ensure the score reflects a fair balance across all evaluation aspects (education, experience, hard skills, certificates, soft skills).
3. All aspects must be rated based on how well they fit the specific job description.
4. The entire evaluation must be in English and formatted as JSON.

"""

RETURN_FORMAT_PROMPT = """

ONLY RESPONSE IN THIS OUTPUT FORMAT JSON LIKE BELOW NOTHING ELSE INCLUDED:
```{
"education_degree": [],
"experience": 0.0,
"technicial_skill": [],
"certificates": [],
"soft_skill": [],
"summary_cv": "",
"fit_score": 0.0,
"explanation": ""
}```
"""

def build_ai_prompt(resume_text: str, job_description: str, custom_prompt: str) -> str:
    """
    Constructs the full AI prompt using the job description and resume text.
    """
    return (
        SCORING_SYSTEM_PROMPT
        + "\nUSER: " + custom_prompt
        + RETURN_FORMAT_PROMPT
        + "\nCONTENT:\nHere is the resume:\n" + resume_text
        + "\n\nHere is the job description:\n" + job_description
    )

def call_ai_model(model_prompt: str):
    """
    Calls the AI model with the given prompt and returns the response.
    """
    try:
        response_content, cost, input_tokens, output_tokens = common.SELECTED_MODEL.call(
            response_format="text",
            messages=[{"role": "user", "content": model_prompt}]
        )

        # Log AI model output
        log.print_llm(f"Cost: {cost}, Input Tokens: {input_tokens}, Output Tokens: {output_tokens}")
        log.print_llm(f"Model Response: {response_content}")

        return response_content

    except Exception as e:
        log.print_error(f"AI request failed: {e}")
        return None, None, None, None
    
    
def parse_ai_response(response_content: str):
    """
    Parses the AI response and ensures valid JSON format.
    """
    response_data = util.data_filter(response_content)
    
    if not response_data:
        log.print_error("AI returned invalid JSON. Skipping resume.")
        return None

    return response_data
