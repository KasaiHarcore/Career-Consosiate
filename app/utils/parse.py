import os
from app.model import common
from app import log, globals
from app.utils import util

def parse_resumes(folder_path, data, job_des, custom_prompt = ""):
    for i in range(len(data)):
        file_path = data['File'][i]
        file_name = os.path.basename(file_path)

        resume = data["Resume"][i]
        log.print_with_time(f"Processing resume {i}...")
        try:
            # Call the model
            response_content, cost, input_tokens, output_tokens = common.SELECTED_MODEL.call(
                response_format = "text",
                messages = [
                    {
                    "role": "user",
                    "content": globals.scoring_system_prompt + "\nUSER:" + custom_prompt + "\nCONTENT: \nHere is the resume:\n" + resume + "\n" + "\n\nHere is the job description:\n" + job_des
                    }
                ]
            )

            log.print_llm(f"Cost: {cost}, Input tokens: {input_tokens}, Output tokens: {output_tokens}")
            log.print_llm(f"Response: {response_content}")
            # Parse the response
            response = util.data_filter(response_content)
            data["Education"][i] = response["Education"]
            data["Experience"][i] = response["Experience"]
            data["Technical Skills"][i] = response["Technical Skills"]
            data["Certificates"][i] = response["Certificates"]
            data["Soft Skills"][i] = response["Soft Skills"]
            data["Summary"][i] = response["Summary Comment"]
            data["Score"][i] = response["Score"]
            data["Explanation"][i] = response["Explanation"]

        except Exception as e:
            log.print_error(f"Error processing resume {i}: {e}")
            globals.failed.append(file_name)
            continue
 
    return True