
import fitz

pdf_path = "books/Siddhartha.pdf.pdf"

# Open the PDF
document = fitz.open(pdf_path)

# PDF page 13 (zero-based index 12)
page = document[12]

# Extract text using PyMuPDF
text = page.get_text("text")

print("Extracted using PyMuPDF:\n")
print(text)

print("\nChecking important words:\n")

words = ["fine", "official", "offering", "flowing", "suffice"]

for word in words:
    print(f"{word}: {word in text.lower()}")

document.close()
