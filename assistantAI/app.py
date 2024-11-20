from openai import OpenAI
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))


API_KEY=""

file_path = (os.path.dirname(__file__))+"/data.txt"
client = OpenAI(api_key=API_KEY)


# # Create a vector store caled "English phrasal verbs"
# vector_store = client.beta.vector_stores.create(name="English phrasal verbs")
 
# # Ready the files for upload to OpenAI
# file_paths = [file_path]
# file_streams = [open(path, "rb") for path in file_paths]
 
# # Use the upload and poll SDK helper to upload the files, add them to the vector store,
# # and poll the status of the file batch for completion.
# file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
#   vector_store_id=vector_store.id, files=file_streams
# )
 
# # You can print the status and the file counts of the batch to see the result of this operation.
# print(file_batch.status)
# print(file_batch.file_counts)




#TO - DO , this should be put into another file

# system_prompt = """You are an assistant for question-answering tasks. \
# Use the following pieces of retrieved context to answer the question, questions must be related to phrasal verbs \
# If you don't know the answer, just say that you don't know. \
# Use three sentences maximum and keep the answer concise.\
# """

# assistant = client.beta.assistants.create(
#     instructions=system_prompt,
#     name="Math Tutor",
#     tools=[{"type": "file_search"}],
#     model="gpt-3.5-turbo",
# )
# print(assistant)


# assistant = client.beta.assistants.update(
#   assistant_id=assistant.id,
#   tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
# )



thread = client.beta.threads.create()


message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="I need to help me giving three example of phrasal verbs?"
)


from typing_extensions import override
from openai import AssistantEventHandler

assistant = client.beta.assistants.retrieve("")
print(assistant)
 
# First, we create a EventHandler class to define
# how we want to handle the events in the response stream.
 
class EventHandler(AssistantEventHandler):    
  @override
  def on_text_created(self, text) -> None:
    print(f"\nassistant > ", end="", flush=True)
      
  @override
  def on_text_delta(self, delta, snapshot):
    print(delta.value, end="", flush=True)
      
  def on_tool_call_created(self, tool_call):
    print(f"\nassistant > {tool_call.type}\n", flush=True)
  
  def on_tool_call_delta(self, delta, snapshot):
    if delta.type == 'file_search':
      if delta.file_search.input:
        print(delta.file_search.input, end="", flush=True)
      if delta.file_search.outputs:
        print(f"\n\noutput >", flush=True)
        for output in delta.file_search.outputs:
          if output.type == "logs":
            print(f"\n{output.logs}", flush=True)
 
# Then, we use the `stream` SDK helper 
# with the `EventHandler` class to create the Run 
# and stream the response.
 
with client.beta.threads.runs.stream(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="Please address the user as Jane Doe. The user has a premium account.",
  event_handler=EventHandler(),
) as stream:
  stream.until_done()