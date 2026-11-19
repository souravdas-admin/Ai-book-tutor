import chromadb
import requests
import json
from sentence_transformers import SentenceTransformer

conversation_history = []
# Load embedding model
print("Loading embedding model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
print("Embedding model loaded!")


# Connect to ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_collection(name="siddhartha_book")


# Ollama API
ollama_url = "http://localhost:11434/api/chat"




def rewrite_question(question):

    # If there is no conversation history, use the original question
    if not conversation_history:
        return question

    # Get the last few conversation messages
    recent_messages = conversation_history[-6:]

    # Collect previous user questions
    previous_questions = []

    for message in recent_messages:
        if message["role"] == "user":
            previous_questions.append(message["content"])

    # Check whether the current question contains pronouns
    pronoun_words = ["he", "she", "him", "her", "they", "them", "it"]

    words = question.lower().split()

    contains_pronoun = any(
        word.strip("?.!,") in pronoun_words
        for word in words
    )

    # If it is a follow-up, combine the last two questions with it
    if contains_pronoun and previous_questions:
        context_questions = previous_questions[-2:]

        search_query = " ".join(context_questions + [question])

        return search_query

    return question


def ask_book(question):

    # Convert question into embedding
    # Convert follow-up into a contextual search query
    search_query = rewrite_question(question)

    print("\nOriginal question:", question)
    print("Search query:", search_query)

# Generate embedding from contextual search query
    question_embedding = embedding_model.encode(search_query).tolist()
    # Retrieve relevant chunks
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=3
    )

    retrieved_chunks = results["documents"][0]
    distances = results["distances"][0]

    # Combine retrieved passages
    context = "\n\n".join(retrieved_chunks)

    # Create prompt
    prompt = f"""
/no_think

Answer the user's question using ONLY the provided context.

If a follow-up question refers to an earlier message,
use the conversation history to understand it.

If the answer is not present in the context, say so clearly.
Distinguish facts from interpretation.
Keep your answer concise and easy to understand.

CONTEXT:
{context}

QUESTION:
{question}
"""

    # Add latest question to conversation history
    conversation_history.append({
        "role": "user",
        "content": question
    })

    # Prepare messages for Ollama
    messages = [
        {
            "role": "system",
            "content": "You are an AI tutor for Siddhartha by Hermann Hesse."
        }
    ] + conversation_history[:-1] + [
        {
            "role": "user",
            "content": prompt
        }
    ]

    # Prepare request
    payload = {
        "model": "qwen3:4b",
        "messages": messages,
        "think": False,
        "stream": True,
        "options": {
            "num_predict": 300,
            "temperature": 0.3
        }
    }

    # Display retrieved sources
    print("\n" + "=" * 50)
    print("SOURCES RETRIEVED")
    print("=" * 50)

    for i, source in enumerate(retrieved_chunks, start=1):

        distance = distances[i - 1]

        print(f"\n--- Source {i} | Distance: {distance:.4f} ---")
        print(source[:500])
        print("...")

    # Generate AI answer
    print("\nAI Tutor: ", end="", flush=True)

    assistant_answer = ""

    # Send request and receive streaming response
    with requests.post(
        ollama_url,
        json=payload,
        stream=True,
        timeout=(10, 300)
    ) as response:

        response.raise_for_status()

        for line in response.iter_lines():

            if line:

                data = line.decode("utf-8")
                chunk = json.loads(data)

                content = chunk.get("message", {}).get("content", "")

                if content:
                    print(content, end="", flush=True)
                    assistant_answer += content

    # Save AI response to conversation history
    conversation_history.append({
        "role": "assistant",
        "content": assistant_answer
    })

    print("\n")
    return assistant_answer




