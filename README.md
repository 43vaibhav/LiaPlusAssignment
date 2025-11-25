# Emotional Intelligence Chatbot

**Assignment:** Conversational AI with Sentiment Analysis (Tier 1 & Tier 2 Implementation)

A production-grade Python chatbot that maintains full conversation history, performs real-time sentiment analysis on individual user messages, and generates comprehensive emotional journey summaries. Built with **Google Gemini** for intelligent responses and **VADER** for accurate sentiment evaluation. This version adds a small web UI and a FastAPI HTTP endpoint so the bot can be used from a browser or programmatically.

---

## Implementation Status

### ✅ Tier 1 – Mandatory Requirement: Conversation-Level Sentiment Analysis
- **Full conversation history** maintained throughout the interaction
- **Final sentiment analysis** generated at the end of conversation
- **Overall emotional direction** clearly indicated based on complete exchange
- Status: **COMPLETE** ✓

### ✅ Tier 2 – Additional Credit: Statement-Level Sentiment Analysis
- **Individual sentiment evaluation** for every user message
- **Real-time sentiment display** alongside each message with emoji indicators:
  - Positive 😊 (compound score ≥ 0.05)
  - Neutral 😐 (compound score between -0.05 and 0.05)
  - Negative 😔 (compound score ≤ -0.05)
- **Mood trend summarization** with intelligent insights about conversation arc
- **Advanced metrics**: mood swings, peak emotions, average sentiment, mood recovery patterns
- Status: **COMPLETE** ✓

### 🎁 Bonus Features
- Empathetic AI responses using Google Gemini with custom system prompt
- Multi-metric mood tracking (peak joy, peak frustration, consistency analysis)
- Natural language insights about emotional patterns
- Production-ready error handling and modular code structure
- Comprehensive unit tests for sentiment analyzer

---

## How to Run

### 1. Prerequisites
- Python 3.8+
- Google Gemini API Key (free at [Google AI Studio](https://aistudio.google.com/app/apikey))
- Internet connection

### 2. Installation

**Clone/Set Up the Project:**
```bash
cd Chatbot1
```

**Create Virtual Environment (Windows PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Create Virtual Environment (macOS/Linux):**
```bash
python -m venv .venv
source .venv/bin/activate
```

**Install Dependencies:**
```bash
pip install -r requirements.txt
```

### 3. Configuration

**Get a Gemini API Key:**
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your key

**Create `.env` File:**
```env
GEMINI_API_KEY=your_api_key_here
```

**⚠️ Security:** `.env` is in `.gitignore` — never commit it!

### 4. Run the Chatbot

There are two ways to run the project:

1) Run as a console application (present in `chatbot.py`):

```bash
python chatbot.py
```

2) Run as a web service (recommended for the web UI):

Install the web dependencies and start `uvicorn` to serve the FastAPI app in `chatbot.py`.

```bash
# start the FastAPI app (development mode with autoreload)
uvicorn chatbot:app --reload --host 127.0.0.1 --port 8000
```

The FastAPI app exposes a POST `/chat` endpoint which accepts JSON `{"text":"..."}` and returns a JSON reply including sentiment, score, and whether the conversation ended.

The repository also includes a simple `index.html` in the project root that demonstrates how to call the `/chat` endpoint from a browser.

---

## Example Usage

```
Gemini + Emotional Intelligence Chatbot (Updated for 2025)
Type 'exit', 'quit', or 'bye' to end and see your emotional journey.

You: Your service disappoints me
→ Mood: Negative 😔 (-0.627)

Gemini: I'm truly sorry to hear that you're feeling disappointed. Your feedback is valuable
to us, and I want to help make things right. Can you tell me more about what happened?

You: Last experience was better
→ Mood: Positive 😊 (+0.518)

Gemini: I'm glad you've had better experiences with us before. Let's work together to bring
that same level of quality back. What specifically made that experience better?

You: exit
```

---

## Final Output Example

When you type `exit`, `quit`, or `bye`, you'll see a comprehensive summary:

```
======================================================================
          YOUR EMOTIONAL JOURNEY SUMMARY
======================================================================
Final Mood: Positive

Mood Journey: Negative → Positive
• Mood swings: 1
• Peak joy: +0.518 | Peak frustration: -0.627
• Average sentiment: -0.0545
• Insight: Amazing recovery! Started negative but ended on a high note.

Messages analyzed: 2
======================================================================
Take care! Come back anytime 💙
```

---

## Chosen Technologies

| Technology | Purpose | Why Chosen |
|-----------|---------|-----------|
| **Python 3.8+** | Core language | Simplicity, readability, industry standard for NLP |
| **Google Gemini API** | AI responses | Free tier available, state-of-the-art language model |
| **VADER** | Sentiment analysis | Specialized for social media/conversational text, fast, accurate |
| **FastAPI** | HTTP server & web UI backend | Lightweight, high-performance ASGI framework used to expose `/chat` endpoint |
| **uvicorn** | ASGI server | Fast, standard runner for FastAPI during development |
| **python-dotenv** | Config management | Secure API key handling, environment isolation |
| **unittest** | Testing | Built-in, no external dependencies, industry standard |

---

## Sentiment Analysis Logic

### VADER (Valence Aware Dictionary and sEntiment Reasoner)

**Why VADER?**
- Designed for social media and conversational text (perfect for chatbot messages)
- Lexicon-based: uses a pre-built dictionary of sentiment words with intensities
- Handles punctuation, capitalization, and context modifiers (e.g., "very good")
- Fast and lightweight — no neural network overhead
- Highly interpretable — scores directly represent emotional intensity

**Scoring System:**
- Returns a compound score ranging from -1.0 (most negative) to +1.0 (most positive)
- Threshold-based classification:
  - **Negative**: compound ≤ -0.05
  - **Neutral**: -0.05 < compound < +0.05
  - **Positive**: compound ≥ +0.05

**Example Analysis:**
```python
Text: "Your service disappoints me"
Scores: {'neg': 0.469, 'neu': 0.531, 'pos': 0.0, 'compound': -0.627}
→ Classification: Negative 😔

Text: "That's wonderful!"
Scores: {'neg': 0.0, 'neu': 0.228, 'pos': 0.772, 'compound': 0.798}
→ Classification: Positive 😊
```

### Statement-Level vs. Conversation-Level Analysis

**Statement-Level (Tier 2):**
- Each user message analyzed independently
- Real-time sentiment score displayed immediately
- Captures moment-to-moment emotional shifts

**Conversation-Level (Tier 1):**
- All user messages combined into full transcript
- Overall compound score averaged across all statements
- Provides macro emotional trend and insights

---

## Project Structure

```
Chatbot1/
├── chatbot.py              # Main application (GeminiChatbot + SentimentAnalyzer classes)
├── test_sentiment.py       # Unit tests for SentimentAnalyzer
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── .env                    # API keys (not in version control)
├── .gitignore              # Git exclusion rules
└── .venv/                  # Virtual environment
```

---

## Testing

Run the sentiment analyzer unit tests:

```bash
python -m unittest test_sentiment.py -v
```

**Expected Output:**
```
test_negative ... ok
test_positive ... ok
test_trend ... ok
----------------------------------------------------------------------
Ran 3 tests in 0.075s

OK
```

**Tests Verify:**
- Positive sentiment correctly identified (e.g., "I love this!" → Positive)
- Negative sentiment correctly identified (e.g., "This sucks." → Negative)
- Mood trend tracking across multiple messages

---

## Configuration & Customization

### Change Gemini Model

Edit `chatbot.py`:
```python
MODEL_NAME = "gemini-2.5-pro"  # Options: gemini-2.5-flash, gemini-2.5-pro, gemini-1.5-pro
```

### Adjust Response Generation

Edit `get_response()` method:
```python
generation_config=genai_types.GenerationConfig(
    temperature=0.8,          # 0.0–2.0 (higher = more creative)
    max_output_tokens=600     # Response length limit
)
```

### Customize System Prompt

Edit `GeminiChatbot.__init__()`:
```python
system_instruction="You are a warm, empathetic, and caring support assistant. "
                  "Respond with kindness, patience, and understanding."
```

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| `GEMINI_API_KEY not found` | Create `.env` with your API key |
| `404 Model not found` | Update `MODEL_NAME` to valid Gemini model |
| `Rate limit exceeded` | Wait before next request or upgrade API plan |
| Incorrect sentiment score | VADER works best with standard English; avoid excessive misspellings |
| `ModuleNotFoundError: fastapi` or `uvicorn` | Install the web dependencies from `requirements.txt` or run `pip install fastapi uvicorn` |

---

## Dependencies

This project can run as a console app or a small web service. The dependencies below include the web stack used by the FastAPI-based UI.

- **google-generativeai** ≥ 0.8.0 — Gemini API client
- **vaderSentiment** ≥ 3.3.2 — Sentiment analysis
- **python-dotenv** ≥ 1.0.0 — Environment variable management
- **fastapi** ≥ 0.95.0 — Web framework for the `/chat` endpoint
- **uvicorn** ≥ 0.22.0 — ASGI server to run FastAPI

Install all:
```bash
pip install -r requirements.txt
```

Install all:
```bash
pip install -r requirements.txt
```

---

## Submission Checklist

- ✅ **Source Code**: `chatbot.py`, `test_sentiment.py`
- ✅ **README**: Technologies, how to run, sentiment logic, Tier 1 & 2 status
- ✅ **Tests**: `test_sentiment.py` with 3 passing test cases
- ✅ **Git Repository**: `.gitignore` configured, clean history
- ✅ **Tier 1 Implementation**: Conversation-level sentiment + final report
- ✅ **Tier 2 Implementation**: Statement-level sentiment + mood trends
- ✅ **Bonus Features**: Empathetic AI, mood metrics, natural insights

---

## License

This project is open-source and available for educational and personal use.

---

**Built with ❤️ | Gemini + VADER + Python**
