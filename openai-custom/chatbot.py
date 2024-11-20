from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from knowledgePinecone import docsearch
from dotenv import load_dotenv, dotenv_values 
import os

load_dotenv()

llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model_name="gpt-3.5-turbo",
    temperature=0.0
)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=docsearch.as_retriever()
)


query1 = "What are the first 3 steps for getting started with the WonderVector5000?"

query2 = "The Neural Fandango Synchronizer is giving me a headache. What do I do?"


query1_with_knowledge = qa.invoke(query1)
query1_without_knowledge = llm.invoke(query1)

print(query1_with_knowledge)
print()
print(query1_without_knowledge)

# Response:
# {'query': 'What are the first 3 steps for getting started with the WonderVector5000?', 'result': "The first 3 steps for getting started with the WonderVector5000 are:\n\n1. Unpack the Device: Remove the WonderVector5000 from its anti-gravitational packaging with care.\n2. Initiate the Quantum Flibberflabber Engine: Pull the translucent lever marked “QFE Start” gently to engage the engine.\n3. Calibrate the Hyperbolic Singularity Matrix: Turn the dials labeled 'Infinity A' and 'Infinity B' until the matrix stabilizes with a single, stable “∞” display."}
#
# content='1. Unbox the WonderVector5000 and carefully read the user manual provided. Familiarize yourself with the different components of the device and understand their functions.\n\n2. Charge the WonderVector5000 using the provided charging cable. Make sure the device is fully charged before using it for the first time to ensure optimal performance.\n\n3. Turn on the WonderVector5000 by pressing the power button. Follow the on-screen instructions to set up the device and customize the settings according to your preferences.' response_metadata={'token_usage': {'completion_tokens': 100, 'prompt_tokens': 24, 'total_tokens': 124}, 'model_name': 'gpt-3.5-turbo', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-e782f1a1-3c1a-436f-bfb7-ca39552d8761-0'    
