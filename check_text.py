
from book_reader import get_page

# Inspect page 2 of Chapter 1
page = get_page("The Brahmin's Son", 2)

print("Extracted text:")
print(repr(page["content"]))

print("\nChecking for replacement characters:")

if "\uFFFD" in page["content"]:
    print("Replacement characters found!")
else:
    print("No Unicode replacement characters found.")
