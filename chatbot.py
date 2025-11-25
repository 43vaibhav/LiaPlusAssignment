# chatbot.py
import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai
import google.generativeai.types as genai_types  # Explicit import for config

load_dotenv()

# === Gemini Setup ===
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY not found in .env file!")
    print("Get your key from: https://aistudio.google.com/app/apikey")
    sys.exit(1)

genai.configure(api_key=GEMINI_API_KEY)

# UPDATED: Use the current stable model (2025 standard)
MODEL_NAME = "gemini-2.5-flash-lite"  # Fast, stable, and supported

# === VADER ===
try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
except ImportError:
    print("Run: pip install vaderSentiment")
    sys.exit(1)


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
        shifts = [(i, labels[i-1], labels[i]) for i in range(1, len(labels)) if labels[i] != labels[i-1]]

        start = labels[0]
        end = labels[-1]
        avg = round(sum(scores) / len(scores), 3)
        peak_pos = max(scores)
        peak_neg = min(scores)
        swings = len(shifts)

        # Natural language insight
        if swings == 0:
            insight = f"Very stable mood — stayed consistently {start.lower()}."
        elif end == "Positive" and start == "Negative":
            insight = "Amazing recovery! Started negative but ended on a high note."
        elif end == "Negative" and start == "Positive":
            insight = "The mood deteriorated over time — ended feeling down."
        elif swings >= 3:
            insight = f"Quite emotional with {swings} mood swings."
        else:
            insight = f"Some ups and downs, but ended {end.lower()}."

        trend = f"{start} → {end}" if start != end else start

        return (
            f"Mood Journey: {trend}\n"
            f"• Mood swings: {swings}\n"
            f"• Peak joy: {peak_pos:+.3f} | Peak frustration: {peak_neg:+.3f}\n"
            f"• Average sentiment: {avg:+.3f}\n"
            f"• Insight: {insight}"
        )


class GeminiChatbot:
    def __init__(self):
        try:
            self.model = genai.GenerativeModel(
                model_name=MODEL_NAME,
                system_instruction="You are a warm, empathetic, and caring support assistant. "
                                  "Respond with kindness, patience, and understanding."
            )
        except Exception as e:
            print(f"Model init error: {e}")
            print("Try updating to: MODEL_NAME = 'gemini-2.5-pro' in the code.")
            sys.exit(1)
        
        # Start a proper chat session
        self.chat_session = self.model.start_chat(history=[])
        self.sentiment = SentimentAnalyzer()

    def get_response(self, user_input):
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

    def chat(self):
        print("Gemini + Emotional Intelligence Chatbot (Updated for 2025)")
        print("Type 'exit', 'quit', or 'bye' to end and see your emotional journey.\n")

        while True:
            msg = input("You: ").strip()
            if msg.lower() in ["exit", "quit", "bye"]:
                break
            if not msg:
                continue

            # Analyze sentiment
            label, conf = self.sentiment.analyze(msg)
            emoji = {"Positive": "😊", "Negative": "😔", "Neutral": "😐"}[label]
            print(f"→ Mood: {label} {emoji} ({conf:+.3f})\n")

            # Get reply from Gemini
            reply = self.get_response(msg)
            print(f"Gemini: {reply}\n")

        # === FINAL REPORT ===
        print("\n" + "═" * 70)
        print("          YOUR EMOTIONAL JOURNEY SUMMARY")
        print("═" * 70)
        if self.sentiment.user_scores:
            final_score = self.sentiment.user_scores[-1]
            final_mood = 'Positive' if final_score >= 0.05 else 'Negative' if final_score <= -0.05 else 'Neutral'
            print(f"Final Mood: {final_mood}\n")
            print(self.sentiment.get_enhanced_trend_summary())
            print(f"\nMessages analyzed: {len(self.sentiment.user_scores)}")
        else:
            print("No messages sent.")
        print("═" * 70)
        print("Take care! Come back anytime 💙\n")


if __name__ == '__main__':
    GeminiChatbot().chat()