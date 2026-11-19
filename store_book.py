from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb

# 1. Read the PDF
pdf_path = "books/Siddhartha.pdf.pdf"

reader = PdfReader(pdf_path)

book_text = ""

for page in reader.pages:
    text = page.extract_text()

    if text:
        book_text += text + "\n"


# 2. Divide text into chunks
chunk_size = 1000
overlap = 200

chunks = []

start = 0

while start < len(book_text):
    end = start + chunk_size

    chunk = book_text[start:end]

    chunks.append(chunk)

    start = end - overlap

print("Total chunks:", len(chunks))


# 3. Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# 4. Generate embeddings
embeddings = model.encode(
    chunks,
    show_progress_bar=True
)


# 5. Create persistent ChromaDB database
client = chromadb.PersistentClient(path="./chroma_db")


# 6. Create a collection
collection = client.get_or_create_collection(
    name="siddhartha_book"
)


# 7. Store chunks, embeddings and IDs
collection.upsert(
    ids=[str(i) for i in range(len(chunks))],
    documents=chunks,
    embeddings=embeddings.tolist()
)


print("\nBook successfully stored in ChromaDB!")

print("Total documents stored:", collection.count())