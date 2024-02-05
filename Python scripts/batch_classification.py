

#################
#######
## with tags

from typing import List
import asyncio
from pydantic import BaseModel, model_validator, ValidationInfo
import openai
import instructor

client = instructor.patch(
    openai.AsyncOpenAI(),
)

class Tag(BaseModel):
    id: int
    name: str

    @model_validator(mode="after")
    def validate_ids(self, info: ValidationInfo):
        context = info.context
        if context:
            tags: List[Tag] = context.get("tags")
            assert self.id in {
                tag.id for tag in tags
            }, f"Tag ID {self.id} not found in context"
            assert self.name in {
                tag.name for tag in tags
            }, f"Tag name {self.name} not found in context"
        return self


class TagWithInstructions(Tag):
    instructions: str


class TagRequest(BaseModel):
    texts: List[str]
    tags: List[TagWithInstructions]


class TagResponse(BaseModel):
    texts: List[str]
    predictions: List[Tag]


async def tag_single_request(request: TagRequest) -> TagResponse:
    allowed_tags = [(tag.id, tag.name) for tag in request.tags]
    allowed_tags_str = ", ".join([f"`{tag}`" for tag in allowed_tags])

    return await client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {
                "role": "system",
                "content": "You are a world-class text tagging system.",
            },
            {"role": "user", "content": f"Describe the following details:\nAuthor Names: {', '.join(request.author_names)}\nPaper Title: {request.paper_title}\nYear of Publication: {request.year_of_publication}\nAPA Citation: {request.apa_citation}"},
            {
                "role": "user",
                "content": f"Here are the allowed tags: {allowed_tags_str}",
            },
        ],
        response_model=Tag,  
        validation_context={"tags": request.tags},
    )

async def tag_single_request(text: str, tags: List[Tag]) -> Tag:
    allowed_tags = [(tag.id, tag.name) for tag in tags]
    allowed_tags_str = ", ".join([f"`{tag}`" for tag in allowed_tags])

    return await client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {
                "role": "system",
                "content": "You are a world-class text tagging system.",
            },
            {"role": "user", "content": f"Describe the following text: `{text}`"},
            {
                "role": "user",
                "content": f"Here are the allowed tags: {allowed_tags_str}",
            },
        ],
        response_model=Tag,  # Minimizes the hallucination of tags that are not in the allowed tags.
        validation_context={"tags": tags},
    )


async def tag_request(request: TagRequest) -> TagResponse:
    predictions = await asyncio.gather(
        *[tag_single_request(text, request.tags) for text in request.texts]
    )
    return TagResponse(
        texts=request.texts,
        predictions=predictions,
    )

# Example usage
tags = [
    TagWithInstructions(id=0, name="author", instructions="Author names"),
    TagWithInstructions(id=1, name="title", instructions="Paper title"),
    TagWithInstructions(id=2, name="year", instructions="Year of publication"),
    TagWithInstructions(id=3, name="APA", instructions="APA citation"),
]

paper_list = []

with open('data/Referencias Machine Learning.docx.txt', 'r') as file:
    for line in file:
        # Remove leading and trailing whitespaces
        paper_info = line.strip()
        # Add paper information to the list
        paper_list.append(paper_info)



texts = paper_list[0:5]

request = TagRequest(texts=texts, tags=tags)

# The response will contain the texts, the predicted tags, and the confidence.
response = asyncio.run(tag_request(request))
print(response.model_dump_json(indent=2))
