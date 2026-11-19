
import json
import pymupdf


# STEP 1: Extract pages from PDF
def extract_book():

    pdf_path = "books/Siddhartha.pdf.pdf"
    reader = pymupdf.open(pdf_path)

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

    book_data = {}

    for chapter_name, (start_page, end_page) in chapters.items():

        chapter_pages = []

        for pdf_page in range(start_page, end_page + 1):

            page = reader[pdf_page - 1]
            page_text = page.get_text("text")

            if page_text:
                chapter_pages.append({
        "page_number": pdf_page - start_page + 1,
        "pdf_page": pdf_page,
        "content": page_text.strip()
    })

            if page_text:
                chapter_pages.append({
                    "page_number": pdf_page - start_page + 1,
                    "pdf_page": pdf_page,
                    "content": page_text.strip()
                })

        book_data[chapter_name] = chapter_pages

    with open("book_pages.json", "w", encoding="utf-8") as file:
        json.dump(book_data, file, ensure_ascii=False, indent=4)

    print("Book extraction completed!")


# STEP 2: Load saved book pages
def load_book():

    with open("book_pages.json", "r", encoding="utf-8") as file:
        return json.load(file)


# STEP 3: Get chapter names
def get_chapter_names():

    book_data = load_book()
    return list(book_data.keys())


# STEP 4: Get all pages of a chapter
def get_chapter_pages(chapter_name):

    book_data = load_book()
    return book_data.get(chapter_name, [])


# STEP 5: Get one particular page
def get_page(chapter_name, page_number):

    pages = get_chapter_pages(chapter_name)

    if 1 <= page_number <= len(pages):
        return pages[page_number - 1]

    return None


# Run extraction only when this file is executed directly
if __name__ == "__main__":
    extract_book()

if __name__ == "__main__":

    page = get_page("The Brahmin's Son", 2)

    print(repr(page["content"]))