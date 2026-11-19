from pypdf import PdfReader

pdf_path = "books/Siddhartha.pdf.pdf"

reader = PdfReader(pdf_path)

total_pages = len(reader.pages)

print("Total pages:", total_pages)

# Store the text of the entire book
book_text = ""

# Read every page
for page in reader.pages:
    text = page.extract_text()

    if text:
        book_text += text + "\n"

print("\nBook successfully extracted!")

print("Total characters:", len(book_text))

print("\nFirst 1000 characters of the book:\n")

print(book_text[:1000])

# Chunking settings
chunk_size = 1000
overlap = 200

chunks = []

start = 0

while start < len(book_text):

    end = start + chunk_size

    chunk = book_text[start:end]

    chunks.append(chunk)

    start = end - overlap

print("\nTotal chunks:", len(chunks))

print("\nFirst chunk:\n")
print(chunks[0])

print("\nSecond chunk:\n")
print(chunks[1])