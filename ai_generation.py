import os
from together import Together
from pypdf import PdfReader
from datetime import datetime
import requests
import json

from bot_role_sumary import BOT_ROLE, HF_TOKEN


API_URL = "https://router.huggingface.co/v1/chat/completions"
    
HEADERS = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json",
    }

PDF_FOLDER = "content/english/publications"
OUTPUT_FOLDER = "temp/"  # Hugo folder

def extract_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text[:8000]  # keep it safe for API limits

# def summarize(text):
#     payload = {
#         "model": "meta-llama/Llama-3.1-8B-Instruct",
#         #"model": "mistralai/Mistral-7B-Instruct-v0.3",
#         "messages": [
#             {'role': 'system', 'content': BOT_ROLE},
#             {"role": "user", "content": text}
#         ],
#         "temperature": 0.7,
#         "max_tokens": 500
#     }

#     response = requests.post(API_URL, headers=HEADERS, json=payload)

#     print("Status:", response.status_code)
#     print(response.text)

#     response.raise_for_status()
#     data = response.json()

#     return data["choices"][0]["message"]["content"]

def summarize(text, model="meta-llama/Llama-3.1-8B-Instruct"):
    def build_payload(model, text):
        # Detect Mistral vs chat-based models
        is_mistral = "mistral" in model.lower()

        if is_mistral:
            # Convert to Mistral instruction format
            prompt = f"[INST] {BOT_ROLE}\n\n{text} [/INST]"
            return {
                "model": model,
                "inputs": prompt,
                "parameters": {
                    "temperature": 0.7,
                    "max_new_tokens": 500
                }
            }
        else:
            # Standard OpenAI-style chat (LLaMA etc.)
            return {
                "model": model,
                "messages": [
                    {"role": "system", "content": BOT_ROLE},
                    {"role": "user", "content": text}
                ],
                "temperature": 0.7,
                "max_tokens": 500,
                "response_format": {"type": "json_object"}
            }

    payload = build_payload(model, text)

    response = requests.post(API_URL, headers=HEADERS, json=payload)

    print("Status:", response.status_code)
    print(response.text)

    response.raise_for_status()
    data = response.json()

    # Handle different response formats
    if "choices" in data:
        choice = data["choices"][0]
        return (
            choice.get("message", {}).get("content") or
            choice.get("text")
        )
    elif "generated_text" in data:
        return data["generated_text"]
    else:
        return str(data)

def json_to_html(data):
    return f"""
<p>{data['audience_1']['summary']}</p>

<pre>
{data['audience_1']['quote']}
</pre>

<details class="custom-details">
  <summary><strong>Why This Matters for Scientists</strong></summary>
  <p>{data['audience_2']['part_1']}</p>
</details>

<details class="custom-details">
  <summary><strong>Quick Technical Overview</strong></summary>
  <p>{data['audience_2']['part_2']}</p>

  <pre>
{data['audience_2']['quote']}
  </pre>
</details>

<details class="custom-details">
  <summary><strong>Summary for Policy Makers</strong></summary>
  <p>{data['audience_3']['summary']}</p>

  <pre>
{data['audience_3']['quote']}
  </pre>
</details>

<details class="custom-details">
  <summary><strong>Disclaimer</strong></summary>
  <p>The above summaries were generated with the assistance of an AI system (Mistral).</p>
</details>
"""

def save_markdown(title, content_json):
    filename = title.lower().replace(" ", "-") + ".md"
    path = os.path.join(OUTPUT_FOLDER, filename)
    print(content_json)

    try:
        data = json.loads(content_json)  # will fail if model cheats
    except json.JSONDecodeError:
        print("Invalid JSON:", content_json)
        return
    content = json_to_html(data)
    with open(path, "a") as f:
        f.write(content)

def main():
    for root, dirs, files in os.walk(PDF_FOLDER):
        for file in files:
            if file.lower().endswith(".pdf"):
                path = os.path.join(root, file)
            
                print(f"Processing {file}...")
                text = extract_text(path)
                summary = summarize(text)
                #summary = "Testing append."
                title = file.replace(".pdf", "")
                save_markdown(title, summary)
                variable_not_known

    # os.system("git add .")
    # os.system('git commit -m "auto content update"')
    # os.system("git push")
            break
if __name__ == "__main__":
    main()

