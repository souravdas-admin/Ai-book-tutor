
from pypdf import PdfReader

pdf_path = "books/Siddhartha.pdf.pdf"

reader = PdfReader(pdf_path)

print("Total pages:", len(reader.pages))
print("\nPOSSIBLE CHAPTER HEADINGS\n")

for page_number, page in enumerate(reader.pages, start=1):

    text = page.extract_text()

    if not text:
        continue

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        # Chapter headings are usually short and title-like
        if (
            line
            and len(line) < 40
            and line.istitle()
        ):
            print(f"Page {page_number}: {line}")


# Your existing inspection code above...

print("\nFIRST 24 PDF PAGES\n")

for page_number in range(1, 25):

    page = reader.pages[page_number - 1]
    text = page.extract_text()

    if text:
        lines = text.split("\n")

        print(f"\n--- PDF PAGE {page_number} ---")

        for line in lines[:5]:
            print(line.strip())
