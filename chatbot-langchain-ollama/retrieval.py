from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.storage import LocalFileStore
from langchain.embeddings import CacheBackedEmbeddings


model_name = "text-embedding-3-small"
API_KEY=""

# llm = ChatOpenAI(
#     openai_api_key=API_KEY,
#     model_name="gpt-3.5-turbo",
#     temperature=0.0
# )

# prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are a world class technical documentation writer."),
#     ("user", "{input}")
# ])
from langchain_community.document_loaders import WebBaseLoader
#loader = WebBaseLoader("https://docs.smith.langchain.com/user_guide")
#loader = WebBaseLoader("https://s3.amazonaws.com/remprogram/M2+U1+Phrasal+Verb+Come.pdf")

from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("https://s3.amazonaws.com/remprogram/M2+U1+Phrasal+Verb+Come.pdf")
docs = loader.load()

print(docs)



# from langchain_openai import OpenAIEmbeddings

# embeddings = OpenAIEmbeddings(openai_api_key=API_KEY,  model=model_name)

# store = LocalFileStore("./cache/")

# cached_embedder = CacheBackedEmbeddings.from_bytes_store(
#     embeddings, store, namespace=embeddings.model
# )



# from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter


text_splitter = RecursiveCharacterTextSplitter(separators=".", chunk_size = 100,  chunk_overlap  = 0)
documents = text_splitter.split_documents(docs)

print(f"document:: {documents}")
print(len(documents))
# vector = FAISS.from_documents(documents, embeddings)



# from langchain.chains.combine_documents import create_stuff_documents_chain

# prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

# <context>
# {context}
# </context>

# Question: {input}""")

# document_chain = create_stuff_documents_chain(llm, prompt)




# from langchain.chains import create_retrieval_chain

# retriever = vector.as_retriever()
# retrieval_chain = create_retrieval_chain(retriever, document_chain)


# response = retrieval_chain.invoke({"input": "how can langsmith help with testing?"})
# print(response["answer"])

# LangSmith offers several features that can help with testing:...