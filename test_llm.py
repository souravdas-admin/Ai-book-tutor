import requests

url = "http://localhost:11434/api/chat"

payload = {
    "model": "qwen3:4b",
    "messages": [
        {
            "role": "user",
            "content": "Explain RAG in AI in simple terms."
        }
    ],
    "stream": False
}

response = requests.post(url, json=payload)

result = response.json()

print(result["message"]["content"])