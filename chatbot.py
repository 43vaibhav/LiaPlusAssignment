# chatbot.py — VADER + Gemini + FastAPI (Works with your own index.html)
import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai
import google.generativeai.types as genai_types

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# === VADER ===
try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
except ImportError:
    print("Run: pip install vaderSentiment")
    sys.exit(1)

load_dotenv()

# === Gemini Setup ===
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY not found in .env file!")
    print("Get your key from: https://aistudio.google.com/app/apikey")
    sys.exit(1)

genai.configure(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-2.5-flash-lite"  # Confirmed working in 2025

# === VADER Sentiment Analyzer ===
class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        self.user_scores = []

    def analyze(self, text):
        scores = self.analyzer.polarity_scores(text)
        compound = scores['compound']
        self.user_scores.append(compound)
        label = 'Positive' if compound >= 0.05 else 'Negative' if compound <= -0.05 else 'Neutral'
        return label, round(compound, 3)

    def get_enhanced_trend_summary(self):
        if not self.user_scores:
            return "No conversation yet."

        scores = self.user_scores
        labels = ['Positive' if s >= 0.05 else 'Negative' if s <= -0.05 else 'Neutral' for s in scores]
        shifts = sum(1 for i in range(1, len(labels)) if labels[i] != labels[i-1])

        start, end = labels[0], labels[-1]
        avg = round(sum(scores) / len(scores), 3)
        peak_pos = max(scores)
        peak_neg = min(scores)

        insight = (
            "Amazing recovery! Started negative but ended on a high note." if end == "Positive" and start == "Negative" else
            "The mood went down — I'm here for you." if end == "Negative" and start == "Positive" else
            f"Very emotional with {shifts} mood swings." if shifts >= 3 else
            f"Stable and {start.lower()} throughout." if shifts == 0 else
            f"Ended feeling {end.lower()}."
        )

        trend = f"{start} to {end}" if start != end else start

        return (
            f"Mood Journey: {trend}\n"
            f"• Mood swings: {shifts}\n"
            f"• Peak joy: {peak_pos:+.3f} | Peak low: {peak_neg:+.3f}\n"
            f"• Average: {avg:+.3f}\n"
            f"• Insight: {insight}"
        )

# === Gemini Chatbot ===
class GeminiChatbot:
    def __init__(self):
        self.model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            system_instruction="You are a warm, empathetic, and caring support assistant. "
                              "Respond with kindness, patience, and understanding."
        )
        self.chat_session = self.model.start_chat(history=[])
        self.sentiment = SentimentAnalyzer()

    def get_response(self, user_input: str) -> str:
        try:
            response = self.chat_session.send_message(
                user_input,
                generation_config=genai_types.GenerationConfig(
                    temperature=0.8,
                    max_output_tokens=600
                )
            )
            return response.text.strip()
        except Exception as e:
            return f"[Gemini Error: {str(e)}]"

# === FastAPI App ===
app = FastAPI(title="VADER + Gemini Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Allows your index.html to connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Shared chatbot instance
chatbot = GeminiChatbot()

class Message(BaseModel):
    text: str

@app.post("/chat")
async def chat_endpoint(msg: Message):
    text = msg.text.strip()

    if text.lower() in ["exit", "quit", "bye", "goodbye"]:
        report = chatbot.sentiment.get_enhanced_trend_summary()
        final_score = chatbot.sentiment.user_scores[-1] if chatbot.sentiment.user_scores else 0
        final_mood = 'Positive' if final_score >= 0.05 else 'Negative' if final_score <= -0.05 else 'Neutral'
        
        return {
            "reply": "Thank you for chatting with me today. Take care!",
            "sentiment": final_mood,
            "score": round(final_score, 3),
            "final_report": report,
            "end": True
        }

    # Normal message
    label, score = chatbot.sentiment.analyze(text)
    reply = chatbot.get_response(text)

    return {
        "reply": reply,
        "sentiment": label,
        "score": score,
        "end": False
    }

if __name__ == "__main__":
    print("VADER + Gemini Chatbot Server Running")
    print("Open your index.html file → it will connect automatically!")
    uvicorn.run(app, host="127.0.0.1", port=8000)