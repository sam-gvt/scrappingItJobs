from openai import OpenAI
from dotenv import load_dotenv, dotenv_values
import os
import json


load_dotenv()
def get_all_skills_with_openai(job_description):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"),)

    #(example: Extraction of data based on API is essential, you must return only 'API')
    def parse_unstructured_data():
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "system",
            "content": "Extract the technical skills only from the provided description text and return them in a JSON array named skills."
            },
            {
            "role": "user",
            "content": job_description
            }
        ],
        temperature=0,
        max_tokens=64,
        )

        message_content = response.choices[0].message.content
        response_dict = json.loads(message_content)
        skills_array = response_dict["skills"]


        #print(response.choices[0].message)
        return skills_array
        #response : ChatCompletionMessage(content='{\n    "skills": [\n        "Python",\n        "Typescript",\n        "Django",\n        "Angular",\n        "Postgreql",\n        "SQL",\n        "AWS",\n        "Azure",\n        "GCP",\n        "Kubernetes",\n        "Principes fondamentaux des systèmes distrib', role='assistant', function_call=None, tool_calls=None)

    return parse_unstructured_data()

if __name__ == "__main__":
    get_all_skills_with_openai()