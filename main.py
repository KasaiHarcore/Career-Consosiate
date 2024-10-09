"""
The main driver.
"""

import os
import json
from argparse import ArgumentParser
from collections.abc import Callable, Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from itertools import chain
from os.path import abspath
from os.path import join as pjoin

from loguru import logger

from app import log
from app.model import common
from app.model.register import register_all_models

from env import globals

# Set your GROQ API key securely (avoid hardcoding in production)
os.environ['GROQ_API_KEY'] = "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"

# Register all models
register_all_models()

# Set the desired model
common.set_model("groq/llama-3.1-70b-versatile")

# Define your unstructured text
prompt = """
I graduated with a degree in Computer Science from XYZ University in 2020.
From 2020 to 2022, I worked as a Software Engineer at ABC Corp, where I developed web applications.
Currently, I'm a Senior Developer at DEF Inc., focusing on cloud solutions.
My skills include Python, JavaScript, and AWS services.
I hold certifications in AWS Solutions Architect and Google Cloud Professional.
I'm fluent in English and Spanish.
In 2021, I received the 'Employee of the Year' award at ABC Corp.
"""

# Ensure prompt is a string
prompt = str(prompt)

messages = [
    {
        "role": "user",
        "content": (
            """Extract all JSON-like structures from the following unstructured text. The JSON structures may be inside curly braces {...} or square brackets [...]. Please return them as separate JSON objects or arrays. Text: """
            + prompt
            + """Expected Output:
1. Extract all valid JSON-like structures.
2. Return each extracted structure separately.
3. Ensure the JSON structure is correctly formatted and syntactically valid.
4. Follow the Output Format provided. DO NOT MAKE ANY CHANGES TO THE OUTPUT FORMAT.

Example Output format:
"[
    {"Education": {
        "Major": "...",
        "University": "...",
        "GPA": "..." (optional),
        "Year": "...",
        "Degree": "..." (optional)
    }},
    {"Experience": [{
        "Job Title": "...",
        "Company": "...",
        "Duration": "...",
        "Project": "..."
    }]},
    {"Skills": [...]},
    {"Certifications": [...]},
    {"Languages": [...]},
    {"Achievements": [...]}
]"

Here is an example of the expected output:
[
    {
        "Education": {
            "Major": "Digital Marketing",
            "University": "FPT University",
            "Year": "2021 - Now"
        }
    },
    {
        "Experience": [{
            "Job Title": "Content Collaborator",
            "Duration": "9/2023 - Current",
            "Project": "Quán Fuca Hidden Coffee"
        }]
    },
    {
        "Skills": [
            "Teamwork",
            "Content Writing",
            "Design"
        ]
    },
    {
        "Certifications": [
            "Coursera certifications"
        ]
    },
    {
        "Languages": [
            "Chinese (HSK2)",
            "English"
        ]
    },
    {
        "Achievements": [
            "Increased reach & interaction by 300%",
            "Built a TikTok page with over 6,000 followers"
        ]
    }
]
"""
        ),
    }
]


# Call the model
response_content, cost, input_tokens, output_tokens = common.SELECTED_MODEL.call(
    messages=messages,
    response_format="json_object",
    chat_mode=False
)

# Print the output
print(response_content)
