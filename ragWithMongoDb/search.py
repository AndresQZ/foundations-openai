from embedding import get_embedding

def vector_search(user_query, collection):
    """
    Perform a vector search in the MongoDB collection based on the user query.

    Args:
    user_query (str): The user's query string.
    collection (MongoCollection): The MongoDB collection to search.

    Returns:
    list: A list of matching documents.
    """

    # Generate embedding for the user query
    query_embedding = get_embedding(user_query)

    if query_embedding is None:
        return "Invalid query or embedding generation failed."

    # Define the vector search pipeline
    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "queryVector": query_embedding,
                "path": "plot_embedding_optimised",
                "numCandidates": 150,  # Number of candidate matches to consider
                "limit": 5  # Return top 5 matches
            }
        },
        {
            "$project": {
                 "title": 1,  # Include the title field
                "genres": 1, # Include the genres field,  
            }
        }
    ]

    # Execute the search
    results = collection.aggregate(pipeline)
    return list(results)
