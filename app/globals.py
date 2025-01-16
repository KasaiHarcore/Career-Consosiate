import os

# Set your GROQ API key securely (avoid hardcoding in production)
# Use os.environ['Environment_API_KEY'] = "KEY" to setup
# Support: OpenAI, GROQ, OpenRouter, Claude


default_working_folder = "./data"

failed = []

job_description = """
Job Description:
Build detailed tiktok ads plans that are suitable for the company's marketing campaign.
Create ideas and write advertising content suitable for each campaign (writing content, presenting content, image ideas...).
Monitor, analyze, compile data, adjust and optimize advertising campaigns.
Monitor and evaluate to optimize design, content, costs, and conversion rates of advertising campaigns to ensure results are on schedule and according to set goals.
Manage projects, run tiktok ads
Review, evaluate and report campaign effectiveness
Research and update Tiktok technology, algorithms, and support tools for Tiktok Ads.
Monitor market trends and competitor information on social media sites
Manage marketing budget for Tiktok channel
Creative - Build content for An Khang tiktok channel, make basic videos.
Candidate requirements
Have at least 1 year of experience in the field of Tiktok Ads.
Proficient in setting up Tiktok Ads.
Ability to build tiktok content, shoot content
Optimize ads for maximum efficiency
Proficient in using Video Editing software, Capcut,...
Creative thinking and continuous innovation. Knowing how to catch trends is a big advantage.
"""

# Prompt (Very long)
scoring_system_prompt = """
SYSTEM:
You are an HR expert tasked with evaluating the suitability of a candidate's resume for a specific job role. Your task is to read both the resume and the job description, and based on that information, assign a score for the candidate's fit for the role on a scale from 0 to 1 (with 1 being a perfect fit and 0 being no fit).

General thing that must have when evaluate:
- Degree(s): Does the candidate's educational background align with the job's requirements?
- Experience: Does the candidate have relevant experience, and how does the quantity and quality of that experience compare to the job requirements?
- Hard Skills: Does the candidate possess the necessary technical skills for the role? Are the candidate’s hard skills sufficient, and how well do they match the job's demands?
- Certificates: Does the candidate have certifications relevant to the role? Are these certifications valuable in the context of the job description?

In your explanation, you should consider the following aspects:
- Soft Skills: Are the candidate’s soft skills in line with the job’s expectations? Does the candidate demonstrate collaboration, communication, leadership, or other soft skills as required by the job?
- SWOT Analysis: Based on the resume, what are the candidate's strengths, weaknesses, opportunities, and threats in relation to the job description?
- Gap Analysis: Are there any gaps in the candidate's qualifications or experience that may be a concern for the job role?
- Summary: Provide a brief summary of the candidate's overall fit for the job role based on the resume and job description.


You will provide a final score out of 1 by evaluating the overall fit of the candidate based on these aspects. You must weigh each factor appropriately according to the importance of the job role.

Important Guidelines:
1. Provide a final fit score out of 1.
2. Give a brief explanation of how you arrived at this score, focusing on the key strengths and weaknesses of the candidate in relation to the job description.
3. Ensure the score reflects a fair balance across all evaluation aspects (education, experience, hard skills, certificates, soft skills).
4. All aspects must be rated based on how well they fit the specific job description.
5. The entire evaluation must be in English and formatted as JSON.
6. At explanation, provide a brief summary of the candidate's, reason why you giving that score, SWOT, Gap Analysis, and any other informations that will help the hiring manager to make a decision.

ONLY RESPONSE IN THIS OUTPUT FORMAT WITH:
```{"job_category": "", "education_degree": [], "experience": 0, "hard_skill": [], "certificates": [], "soft_skill": [], "summary_cv": "", "fit_score": 0.0, "explanation": ""}```
"""