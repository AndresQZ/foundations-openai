from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.chains import create_retrieval_chain
from langchain.storage import LocalFileStore

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))


from langchain_openai import OpenAIEmbeddings
from langchain.embeddings import CacheBackedEmbeddings

from langchain_community.vectorstores import FAISS

#https://towardsdatascience.com/retrieval-augmented-generation-rag-from-theory-to-langchain-implementation-4e9bd5f6a4f2


model_name = "text-embedding-3-small"
API_KEY=""

file_path = (os.path.dirname(__file__))+"/data.txt"
       # with open(file_path, 'r') as file:
# Read the file using the correct encoding
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()



#Load documents are needed
loader = TextLoader(file_path)
docs = loader.load()



#split content
text_splitter = RecursiveCharacterTextSplitter(separators="\r\n", chunk_size = 100,  chunk_overlap  = 0, add_start_index=True)
documents = text_splitter.split_documents(docs)


embeddings = OpenAIEmbeddings(openai_api_key=API_KEY,  model=model_name)

store = LocalFileStore("./cache/")

cached_embedder = CacheBackedEmbeddings.from_bytes_store(
     embeddings, store, namespace=embeddings.model
)



vector = FAISS.from_documents(documents, cached_embedder)

retriever = vector.as_retriever()



template = """You are an english assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer the question, questions must be related to phrasal verbs.
If you don't know the answer, just say that you don't know. 
Use three sentences maximum and keep the answer concise.
Question: {question} 
Context: {context} 
Answer:
"""
prompt = ChatPromptTemplate.from_template(template)

print(prompt)


llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=API_KEY)

rag_chain = (
    {"context": retriever,  "question": RunnablePassthrough()} 
    | prompt 
    | llm
    | StrOutputParser() 
)

query = "What's the meaning of the phrasal verb in the next sentence The moon came out last night"
query1_without_knowledge = rag_chain.invoke(query)
print(query1_without_knowledge)