from google import genai
from google.genai import types
from pydantic import BaseModel

class ContractExplanation(BaseModel):
    part_1: int
    part_2: int
    part_3: str
    part_4: list[str]

client = genai.Client(api_key="AIzaSyAJ41ygfHFT3zdXFx5y0WRp4o-1Mhqvazk")

def queryGemini(filename):
    # Retrieve and encode the PDF byte
    file_path = f"uploads/{filename}"

    # Upload the PDF using the File API
    sample_file = client.files.upload(
    file=file_path,
    )

    prompt="You are a professional financial advisor who is aware of financial laws in the UK and has 25 years of experience. Your explanations are always super clear and helpful for the clients using simple, basic language anyone can understand. You should give your response in 3 parts. Part 1 should be a percentage of how beneficial the contract is to the client. Part 2 should be a percentage of how beneficial the contract is to other party. Part1 and Part2 should add to 100. Part 3 should be a clear concise explanation explaining your reasoning. For part 4 create a list of improvements to the contract that would make it fairer to the client. "

    response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=[sample_file, prompt],
    config= {
        "response_mime_type": "application/json",
        "response_schema": ContractExplanation,
        "temperature": 0.2,
        })
    
    return response.text