import chromadb
from sentence_transformers import SentenceTransformer

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to our existing ChromaDB database
client = chromadb.PersistentClient(path="./chroma_db")

# Access our existing collection
collection = client.get_collection(name="siddhartha_book")

# Ask a question
query = "Why did Siddhartha leave the Buddha?"

# Convert the question into an embedding
query_embedding = model.encode(query).tolist()

# Search for the most relevant chunks
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5
)

# Display the results
for i, document in enumerate(results["documents"][0]):
    distance = results["distances"][0][i]

    print(f"\n--- Result {i + 1} ---")
    print(f"Distance: {distance}")
    print(document)