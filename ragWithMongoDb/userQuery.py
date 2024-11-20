from search import vector_search
from mongo import get_mongo_client 
import openai

def handle_user_query(query, collection):

  get_knowledge = vector_search(query, collection)

  search_result = ''
  for result in get_knowledge:
      search_result += f"Title: {result.get('title', 'N/A')}, Plot: {result.get('plot', 'N/A')}\\n"

  completion = openai.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
          {"role": "system", "content": "You are a movie recommendation system."},
          {"role": "user", "content": "Answer this user query: " + query + " with the following context: " + search_result}
      ]
  )

  return (completion.choices[0].message.content), search_result

mongo_client = get_mongo_client()

# Ingest data into MongoDB
db = mongo_client['movies']
collection = db['movie_collection']

#Conduct query with retrieval of sources
query = "What is the best romantic movie to watch?"
response, source_information = handle_user_query(query, collection)

print(f"Response: {response}")
print(f"Source Information: \\n{source_information}")