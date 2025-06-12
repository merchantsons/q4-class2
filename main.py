import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

# Load Gemini API key from .env
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)

def translate_to_urdu(text):
    """
    Translate English text to Urdu script using Gemini 2.0 Flash.
    Strong prompt to enforce proper Urdu script output.
    """
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent"
    headers = {"Content-Type": "application/json"}

    prompt = (
        "You are a professional translator. Translate the following English sentence into standard Urdu script "
        "(using Arabic letters). Do NOT use Roman Urdu. Return only the Urdu translation, no explanations.\n\n"
        f"English: \"{text}\"\nUrdu:"
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    params = {"key": gemini_api_key}

    response = requests.post(url, headers=headers, params=params, json=payload)

    if response.status_code == 200:
        try:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        except (KeyError, IndexError):
            return "Translation error: Unexpected response format."
    else:
        return f"Error {response.status_code}: {response.text}"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        text = request.form.get("text")
        translation = translate_to_urdu(text)
        return jsonify({"translation": translation})
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
else:
    # This is required for Vercel to recognize the app
    application = app
