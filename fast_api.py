import os 
import openai
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
	allow_methods=["GET"],
    allow_origins=["*"],
)

class User_input(BaseModel):
    prompt: str
    key: str

@app.post("/query")
async def query_OpenAI(input: User_input):
    print("I'm here")
    openai.api_key = input.key
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=input.prompt,
        temperature=0.7,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
    # Extracting specific keys from response
    result_stats = dict((k, response[k]) for k in ['id', 'object','created','model','usage']
            if k in response)
    text_out = response.choices[0].text
    print(text_out)
    return JSONResponse(content={'stats': result_stats, 'output': text_out, 'detail': "Successful"})
