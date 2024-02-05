import instructor
import asyncio
import openai
from typing import List
from pydantic import BaseModel
import pandas as pd

paper_list = []

with open('data/Referencias Machine Learning.docx.txt', 'r') as file:
    for line in file:
        # Remove leading and trailing whitespaces
        paper_info = line.strip()
        # Add paper information to the list
        paper_list.append(paper_info)


aclient = instructor.patch(openai.AsyncOpenAI())



class MLPapersExtract(BaseModel):
    author_names: str
    paper_title: str
    year_of_publication: int
    tags: str
    apa_citation: str
    

import asyncio

async def process_paper_citations(paper_citations):
    results = {}

    for i, paper_citation in enumerate(paper_citations, 1):
        task = aclient.chat.completions.create(
            model="gpt-3.5-turbo",
            response_model=MLPapersExtract,
            messages=[
                {"role": "user", "content": f"""
                Extract the necessary information from: {paper_citation}.
                Remember to put all the authors together separated by | and do the same for the tags field.
                """},
            ],
        )

        response = await asyncio.gather(task)
        results[f"paper_{i}"] = response[0].model_dump_json(indent=2)

    return results

# Example usage:
paper_citations = paper_list
result_dict = asyncio.run(process_paper_citations(paper_citations))

# for paper_citation, response_json in result_dict.items():
#     print(f"Paper Citation: {paper_citation}")
#     print(response_json)
#     print("=" * 50)


# Convert dictionary to DataFrame with an index
# Parse the string values into dictionaries
import json
parsed_dict = {key: json.loads(value) for key, value in result_dict.items()}

# Convert to DataFrame
ml_sources_df = pd.DataFrame(list(parsed_dict.values()))

