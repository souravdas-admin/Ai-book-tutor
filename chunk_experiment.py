
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb

# PDF location
pdf_path = "books/Siddhartha.pdf.pdf"

# Load the PDF
reader = PdfReader(pdf_path)

book_text = ""

for page in reader.pages:
    text = page.extract_text()

    if text:
        book_text += text + "\n"

print("Total characters:", len(book_text))

# Load embedding model
print("\nLoading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Embedding model loaded!")


test_questions = [
    "What did Siddhartha learn from the river?",
    "Why did Siddhartha leave Gotama?",
    "Why does Siddhartha believe wisdom cannot be taught?"
]


# Three chunking configurations
experiments = [
    {"name": "Experiment A - Current", "chunk_size": 1000, "overlap": 200},
    {"name": "Experiment B - Smaller", "chunk_size": 500, "overlap": 100},
    {"name": "Experiment C - Larger", "chunk_size": 1500, "overlap": 300}
]

def create_chunks(text, chunk_size, overlap):

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]
        chunks.append(chunk)

        start = end - overlap

    return chunks


# Generate chunks for each experiment
for experiment in experiments:

    chunks = create_chunks(
        book_text,
        experiment["chunk_size"],
        experiment["overlap"]
    )

    print(f"\n{experiment['name']}")
    print("Chunk size:", experiment["chunk_size"])
    print("Overlap:", experiment["overlap"])
    print("Total chunks:", len(chunks))

# Create a temporary ChromaDB client
experiment_client = chromadb.EphemeralClient()

# Store each experiment's chunks and embeddings
for experiment in experiments:

    print(f"\nProcessing {experiment['name']}...")

    # Create chunks
    chunks = create_chunks(
        book_text,
        experiment["chunk_size"],
        experiment["overlap"]
    )

    # Generate embeddings
    embeddings = model.encode(
        chunks,
        show_progress_bar=True
    )

    # Create a separate collection
    collection_name = experiment["name"].split(" - ")[0].lower().replace(" ", "_")
    collection = experiment_client.create_collection(
        name=collection_name
    )

    # Store chunks and embeddings
    collection.add(
        ids=[str(i) for i in range(len(chunks))],
        documents=chunks,
        embeddings=embeddings.tolist()
    )

    print("Stored chunks:", collection.count())

    # Test each question
    for question in test_questions:

        query_embedding = model.encode(question).tolist()

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )

        print("\nQuestion:", question)

        for i, document in enumerate(results["documents"][0]):

            distance = results["distances"][0][i]

            print(f"\nRank {i + 1} | Distance: {distance:.4f}")
            print(document[:350])
            print("-" * 50)
