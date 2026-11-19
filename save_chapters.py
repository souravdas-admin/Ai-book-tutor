
import json
from pypdf import PdfReader

pdf_path = "books/Siddhartha.pdf.pdf"
reader = PdfReader(pdf_path)

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

chapter_texts = {}

for chapter_name, (start_page, end_page) in chapters.items():
    chapter_text = ""

    for page_number in range(start_page - 1, end_page):
        text = reader.pages[page_number].extract_text()

        if text:
            chapter_text += text + "\n"

    chapter_texts[chapter_name] = chapter_text

with open("chapters.json", "w", encoding="utf-8") as file:
    json.dump(chapter_texts, file, ensure_ascii=False, indent=4)

print("Successfully saved all chapters!")
