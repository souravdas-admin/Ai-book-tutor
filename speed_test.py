import requests
import time

url = "http://localhost:11434/api/chat"

payload = {
    "model": "qwen3:4b",
    "messages": [
        {
            "role": "user",
            "content": "In 50 words, explain why Siddhartha left Gotama."
        }
    ],
    "think": False,
    "stream": False,
    "keep_alive": "10m"
}

for test_number in range(1, 4):

    print(f"\n--- Test {test_number} ---")

    start = time.time()

    response = requests.post(url, json=payload)

    result = response.json()

    end = time.time()

    print(result["message"]["content"])

    print(f"\nTotal time: {end - start:.2f} seconds")

    print(f"Model loading time: {result.get('load_duration', 0) / 1e9:.2f} seconds")

    print(f"Prompt processing time: {result.get('prompt_eval_duration', 0) / 1e9:.2f} seconds")

    print(f"Answer generation time: {result.get('eval_duration', 0) / 1e9:.2f} seconds")

    tokens = result.get("eval_count", 0)
    duration = result.get("eval_duration", 0) / 1e9

    if duration > 0:
        print(f"Generation speed: {tokens / duration:.2f} tokens/second")