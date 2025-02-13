import os

# Set your GROQ API key securely (avoid hardcoding in production)
# Use os.environ['Environment_API_KEY'] = "KEY" to setup
# Support: OpenAI, GROQ, OpenRouter, Claude
os.environ['OPENAI_API_KEY'] = ""
os.environ['OPENROUTER_API_KEY'] = "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"
os.environ['GROQ_API_KEY'] = "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"

# Secret Key for Encrypt / Decrypt
# Save this key securely and avoid hardcoding in production
SECURITY_KEY = b'12345678901234567890123456789012' # Must be 32 chars long (256 bits)

# Default Working Folder
default_working_folder = "./data"

# Saving failed CVs parsing
failed = []

# Prompting Section
scoring_system_prompt = """
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
5. At explanation, you're allowed to make more information, state out which part is important or why that score is good, which will help the hiring manager make a decision.
6. **Remember to return the candidate names (Mostly Vietnamese hiding in the context, some with no comma in latin English)**

"""

return_format_prompt = """

ONLY RESPONSE IN THIS OUTPUT FORMAT LIKE BELOW:

{
  "education_degree": [],
  "experience": 0.0,
  "technicial_skill": [],
  "certificates": [],
  "soft_skill": [],
  "summary_cv": "",
  "fit_score": 0.0,
  "explanation": ""
}
"""