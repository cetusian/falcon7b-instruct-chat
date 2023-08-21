import os
import time
#import logging
#from collections import deque
#from typing import Dict, List
#import chromadb
#from chromadb.api.types import Documents, EmbeddingFunction, Embeddings
#import re
import chainlit as cl
import langchain
from langchain import HuggingFaceHub
from langchain import PromptTemplate, LLMChain
from dotenv import load_dotenv
#from chromadb.config import Settings

load_dotenv()

HUGGINGFACEHUB_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN')

repo_id = 'tiiuae/falcon-7b-instruct'

llm =   HuggingFaceHub(huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
                       repo_id=repo_id,
                       model_kwargs={"temperature": 0.6, "max_new_tokens": 500})

template = """Question: {question}

Answer: Let's give you an well-informed answer."""

@cl.on_chat_start
async def main():
    #Instantiate the chain for the user
    elements = [
    cl.Image(name='falcon-llm.jpeg', display='inline', path='/home/madalintat/chat-app/falcon-llm.jpeg')
    ]
    await cl.Message(content="Hello there, I am Falcon 7b Instruct. How can I help you?", elements=elements).send()
    prompt = PromptTemplate(template=template, input_variables=['question'])
    llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=True)

    #Store the chain in the user session
    cl.user_session.set('llm_chain', llm_chain)

@cl.on_message
async def main(message: str):
    #Retrieve the chain from the user session
    llm_chain = cl.user_session.get('llm_chain')

    #Call the chain asynchronously
    res = await llm_chain.acall(message, callbacks=[cl.AsyncLangchainCallbackHandler()])

    #Post processing here

    #Send the response
    await cl.Message(content=res['text']).send()

