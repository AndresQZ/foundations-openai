
# 1. Load Dataset
from datasets import load_dataset
import pandas as pd
from embedding import get_embedding 
from mongo import get_mongo_client 

# https://huggingface.co/datasets/MongoDB/embedded_movies
dataset = load_dataset("MongoDB/embedded_movies")

# Convert the dataset to a pandas dataframe
dataset_df = pd.DataFrame(dataset['train'].select(range(30)))

dataset_df.head(5)


 
print("Columns:", dataset_df.columns)
print("\nNumber of rows and columns:", dataset_df.shape)
print("\nBasic Statistics for numerical data:")
print(dataset_df.describe())
print("\nNumber of missing values in each column:")
print(dataset_df.isnull().sum())


# Remove data point where plot coloumn is missing
dataset_df = dataset_df.dropna(subset=['plot'])
print("\nNumber of missing values in each column after removal:")
print(dataset_df.isnull().sum())

# Remove the plot_embedding from each data point in the dataset as we are going to create new embeddings with the new OpenAI emebedding Model "text-embedding-3-small"
dataset_df = dataset_df.drop(columns=['plot_embedding'])
dataset_df.head(5)

dataset_df["plot_embedding_optimised"] = dataset_df['plot'].apply(get_embedding)

dataset_df.head()


mongo_client = get_mongo_client()

# Ingest data into MongoDB
db = mongo_client['movies']
collection = db['movie_collection']

documents = dataset_df.to_dict('records')
collection.insert_many(documents)

print("Data ingestion into MongoDB completed")