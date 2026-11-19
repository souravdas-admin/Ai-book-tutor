from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Three sentences
sentences = [
    "Siddhartha was searching for enlightenment.",
    "Siddhartha wanted to discover the meaning of life.",
    "The weather was very cold today."
]

# Convert sentences into embeddings
embeddings = model.encode(sentences)

# Compare their meanings
similarity = cosine_similarity(embeddings)

# Display the similarity matrix
print(similarity)