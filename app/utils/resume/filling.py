import pandas as pd
from dateutil import parser
from datetime import datetime

class Resumefiltering:
    """
    
    """
    def __init__(self, data, extract_data):
        self.data = data
        # Initialize an empty DataFrame with the specified columns
        self.extract_data = extract_data

    def extract_information(self):
        # Initialize variables
        education = []
        skills = []
        experience = []
        achievements = []
        year_experiences = 0

        # Extract information from the data
        for item in self.data:
            if 'Education' in item:
                education = item['Education']
            if 'Skills' in item:
                skills = item['Skills']
            if 'Experience' in item:
                experience = item['Experience']

        # Process Education
        if education:
            education_str = f"{education.get('Major', '')} from {education.get('University', '')} with GPA {education.get('GPA', '')}"
        else:
            education_str = None

        # Process Skills
        if skills:
            skills_str = ', '.join(skills)
        else:
            skills_str = None

        # Process Experience and calculate total years of experience
        if experience:
            experience_list = []
            total_experience_months = 0
            for exp in experience:
                # Build experience string
                exp_str = f"{exp.get('Job Title', '')} at {exp.get('Company', '')} ({exp.get('Duration', '')})"
                experience_list.append(exp_str)
                # Calculate duration
                duration = exp['Duration']
                start_str, end_str = duration.split(' - ')
                try:
                    start_date = parser.parse(start_str)
                    if end_str.strip().lower() == 'present':
                        end_date = datetime.now()
                    else:
                        end_date = parser.parse(end_str)
                    months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
                    total_experience_months += months
                except Exception as e:
                    print(f"Error parsing dates: {e}")
                    continue
            experience_str = '; '.join(experience_list)
            year_experiences = round(total_experience_months / 12, 2)  # Convert to years and round off
        else:
            experience_str = None
            year_experiences = 0

        # Assemble the information into a DataFrame row
        data_row = {
            'ID': None,
            'Resume': None,
            'Category': None,
            'Education': education_str,
            'Achievements': achievements,
            'Skills': skills_str,
            'Experience': experience_str,
            'Year Experiences': year_experiences
        }

        # Append the row to the DataFrame
        self.df = self.df.append(data_row, ignore_index=True)

    def get_dataframe(self):
        return self.df