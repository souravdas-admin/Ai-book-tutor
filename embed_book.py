from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

# 1. Read the PDF
pdf_path = "books/Siddhartha.pdf.pdf"

reader = PdfReader(pdf_path)

book_text = ""

for page in reader.pages:
    text = page.extract_text()

    if text:
        book_text += text + "\n"

# 2. Divide the book into chunks
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

# 3. Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 4. Generate embeddings for all chunks
embeddings = model.encode(
    chunks,
    show_progress_bar=True
)

# 5. Display the results
print("\nEmbeddings generated successfully!")

print("Number of chunks:", len(chunks))

print("Embedding shape:", embeddings.shape)

print("\nFirst embedding:")
print(embeddings[0])