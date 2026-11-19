
import json
import requests

# Load all extracted chapters
with open("chapters.json", "r", encoding="utf-8") as file:
    chapters = json.load(file)

print("Chapters loaded:", len(chapters))


def summarize_chapter(chapter_name):

    # Check whether the requested chapter exists
    if chapter_name not in chapters:
        return "Chapter not found."

    # Get the complete text of the selected chapter
    chapter_text = chapters[chapter_name]

    # Prepare the prompt
    prompt = f"""
    You are an expert literature tutor helping a student
    understand Hermann Hesse's novel Siddhartha.

    Summarize the following chapter of Siddhartha:

Chapter title: {chapter_name}

Do not guess or invent the chapter number.

    Follow this structure:

    1. Chapter Overview
    2. Important Events
    3. Key Characters
    4. Important Themes and Philosophical Ideas
    5. What Siddhartha Learns
    6. Important Takeaways

    Use simple English.
    Explain the events clearly.
    Stay faithful to the original chapter.
    Do not invent events or details.

    Chapter Text:
    {chapter_text}
    """

    # Send the request to Ollama
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "qwen3:4b",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 2500
            }
        }
    )

    # Extract the generated summary
    result = response.json()

    summary = result["message"]["content"]

    return summary

if __name__ == "__main__":
    summary = summarize_chapter("The Brahmin's Son")
    print(summary)