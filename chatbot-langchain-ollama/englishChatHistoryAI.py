from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI

from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.storage import LocalFileStore

from langchain_openai import OpenAIEmbeddings
from langchain.embeddings import CacheBackedEmbeddings

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import HumanMessage
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory




from langchain_community.vectorstores import FAISS


import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

model_name = "text-embedding-3-small"
API_KEY=""

embeddings = OpenAIEmbeddings(openai_api_key=API_KEY,  model=model_name)

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



store = LocalFileStore("./cache/")

cached_embedder = CacheBackedEmbeddings.from_bytes_store(
     embeddings, store, namespace=embeddings.model
)



vector = FAISS.from_documents(documents, cached_embedder)

retriever = vector.as_retriever()

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=API_KEY)





contextualize_q_system_prompt = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is."""
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)


qa_system_prompt = """You are an assistant for question-answering tasks. \
Use the following pieces of retrieved context to answer the question, questions must be related to phrasal verbs \
If you don't know the answer, just say that you don't know. \
Use three sentences maximum and keep the answer concise.\

{context}"""
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)


### Statefully manage chat history ###
store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)


conversational_rag_chain.invoke(
    {"input": "What are phrasal verbs?"},
    config={
        "configurable": {"session_id": "abc123"}
    },  # constructs a key "abc123" in `store`.
)["answer"]

ai_msg_3 = conversational_rag_chain.invoke(
    {"input": "Give me an example of a phrasal verb for find?"},
    config={"configurable": {"session_id": "abc123"}},
)["answer"]

print(ai_msg_3["answer"])


chat_history = []

# question = "What are phrasal verbs?"
# ai_msg_1 = rag_chain.invoke({"input": question, "chat_history": chat_history})
# chat_history.extend([HumanMessage(content=question), ai_msg_1["answer"]])

# second_question = "Give me an example of a phrasal verb for find?"
# ai_msg_2 = rag_chain.invoke({"input": second_question, "chat_history": chat_history})
# chat_history.extend([HumanMessage(content=question), ai_msg_2["answer"]])


# third_question = "from the previous questions, give two more examples, create a table to describe those example?"
# ai_msg_3 = rag_chain.invoke({"input": second_question, "chat_history": chat_history})

print(ai_msg_3["answer"])