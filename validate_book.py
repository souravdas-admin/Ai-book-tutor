
import json

with open("book_pages.json", "r", encoding="utf-8") as file:
    book_data = json.load(file)

issues = []

for chapter, pages in book_data.items():
    for page in pages:
        content = page["content"]

        if "\x00" in content or "\uFFFD" in content:
            issues.append({
                "chapter": chapter,
                "pdf_page": page["pdf_page"]
            })

if issues:
    print("Potential extraction issues found:")
    for issue in issues:
        print(issue)
else:
    print("All chapters passed the basic text extraction check!")

print("Total chapters:", len(book_data))
print(
    "Total extracted pages:",
    sum(len(pages) for pages in book_data.values())
)
