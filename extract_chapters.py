
from pypdf import PdfReader

# Load the original PDF
pdf_path = "books/Siddhartha.pdf.pdf"
reader = PdfReader(pdf_path)

# Define chapter boundaries using PDF page numbers
chapters = {
    "The Brahmin's Son": (12, 19),
    "With the Samanas": (20, 28),
    "Gotama": (29, 37),
    "Awakening": (38, 43),
    "Kamala": (44, 64),
    "Sansara": (65, 83),
    "The Ferryman": (84, 94),
    "The Son": (95, 102),
    "Om": (103, 109),
    "Govinda": (110, 119)
}

# Extract each chapter separately
chapter_texts = {}

for chapter_name, (start_page, end_page) in chapters.items():

    chapter_text = ""

    for page_number in range(start_page - 1, end_page):

        page = reader.pages[page_number]
        text = page.extract_text()

        if text:
            chapter_text += text + "\n"

    chapter_texts[chapter_name] = chapter_text

    print(f"\nChapter: {chapter_name}")
    print(f"Pages: {start_page}-{end_page}")
    print(f"Characters extracted: {len(chapter_text)}")

print("\nTotal chapters extracted:", len(chapter_texts))

