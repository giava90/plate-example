import os
import requests
from pypdf import PdfReader
from datetime import datetime

API_KEY = "your_mistral_api_key"

PDF_FOLDER = "content/english/publications"
OUTPUT_FOLDER = "temp/"  # Hugo folder

def extract_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text[:8000]  # keep it safe for API limits

def summarize(text):
    url = "https://api.mistral.ai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistral-small",
        "messages": [
            {"role": "user", "content": f"Summarize this for a blog post:\n\n{text}"}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

def save_markdown(title, content):
    filename = title.lower().replace(" ", "-") + ".md"
    path = os.path.join(OUTPUT_FOLDER, filename)

    md = f"""---
title: "{title}"
date: {datetime.now().isoformat()}
---

{content}
"""
    with open(path, "a") as f:
        f.write(md)

def main():
    for root, dirs, files in os.walk(PDF_FOLDER):
        for file in files:
            if file.lower().endswith(".pdf"):
                path = os.path.join(root, file)
            
                print(f"Processing {file}...")
                text = extract_text(path)
                #summary = summarize(text)
                summary = "Testing append."
                title = file.replace(".pdf", "")
                save_markdown(title, summary)

    os.system("git add .")
    os.system('git commit -m "auto content update"')
    os.system("git push")
    
if __name__ == "__main__":
    main()

