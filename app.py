from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
from groq import Groq   
load_dotenv()
app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
chat_history = []
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data["message"]
    chat_history.append({
        "role": "user",
        "content": user_message
    })
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=chat_history,
        temperature=0.7,
        max_tokens=1024
    )
    bot_reply = completion.choices[0].message.content
    chat_history.append({
        "role": "assistant",
        "content": bot_reply
    })
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
