from django.test import TestCase
from openai import OpenAI
from dotenv import load_dotenv, dotenv_values
import os



class OpenAiTest(TestCase):

    def setUp(self):
        load_dotenv()
        self.client = OpenAI(
          api_key=os.getenv("OPENAI_API_KEY"),
        )

    # def test_openai(self):
    #     completion = self.client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    #         {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
    #     ]
    #     )

    #     print(completion.choices[0].message)


    #(example: Extraction of data based on API is essential, you must return only 'API')
    def test_parse_unstructured_data(self):
        # response = self.client.chat.completions.create(
        # model="gpt-3.5-turbo",
        # messages=[
        #     {
        #     "role": "system",
        #     "content": "Extract from the text provided in JSON the data corresponding to the skills to \
        #                 have in a word "
        #     },
        #     {
        #     "role": "user",
        #     "content": "Développement : Python, Typescript, Django, Angular, Postgreql \
        #                 Développement d’applications évolutives et résilientes,\
        #                 Technologies cloud (AWS, Azure, GCP, Kubernetes),\
        #                 SQL avec des bases de données relationnelles,\
        #                 Principes fondamentaux des systèmes distribués,\
        #                 Extraction de données basés sur API est indispensable.\
        #                 Contexte international : francophone et anglophone."
        #     }
        # ],
        # temperature=0,
        # max_tokens=64,
        # )
        #print(response.choices[0].message)
        pass
        # response : ChatCompletionMessage(content='{\n    "skills": [\n        "Python",\n        "Typescript",\n        "Django",\n        "Angular",\n        "Postgreql",\n        "SQL",\n        "AWS",\n        "Azure",\n        "GCP",\n        "Kubernetes",\n        "Principes fondamentaux des systèmes distrib', role='assistant', function_call=None, tool_calls=None)
