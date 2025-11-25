# Gemini + Emotional Intelligence Chatbot

A conversational AI chatbot that combines **Google Gemini** for natural language processing with **VADER sentiment analysis** to track and understand emotional patterns in conversations.

## Features

- 🤖 **AI-Powered Responses**: Uses Google's Gemini 2.5 Flash Lite model for empathetic, context-aware replies
- 💭 **Real-time Sentiment Analysis**: VADER sentiment analyzer provides instant emotional feedback on user messages
- 📊 **Mood Journey Tracking**: Visualizes emotional trends across the conversation including:
  - Mood shifts and transitions
  - Peak positivity and negativity scores
  - Average sentiment compound score
  - Intelligent insights about conversation tone
- 💙 **Empathetic System**: Built with a caring and supportive system prompt for warm interactions

## Prerequisites

- Python 3.8+
- Google Gemini API Key (free tier available)
- Internet connection (for Gemini API calls)

## Installation

### 1. Clone or Set Up the Project

```bash
cd LiaPlusAssignment
```

### 2. Create and Activate a Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `google-generativeai` — Google Gemini API client
- `vaderSentiment` — Sentiment analysis library
- `python-dotenv` — Environment variable management

## Setup

### Get a Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click **"Create API Key"** → **"Create API key in new project"**
3. Copy the generated API key

### Configure `.env` File

Create or update `.env` in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual Gemini API key.

**⚠️ Security Note:** Never commit `.env` to version control. It's already in `.gitignore`.

## Usage

### Run the Chatbot

```bash
python chatbot.py
```

### Interact with the Chatbot

```
Gemini + Emotional Intelligence Chatbot (Updated for 2025)
Type 'exit', 'quit', or 'bye' to end and see your emotional journey.

You: I'm feeling great today!
→ Mood: Positive 😊 (+0.798)

Gemini: That's wonderful to hear! I'm so glad you're having such a positive day. 
What's making you feel this way? I'd love to hear about it!

You: The weather is beautiful
→ Mood: Positive 😊 (+0.678)

Gemini: Yes! Beautiful weather can really lift our spirits and make everything feel brighter...
```

### Exit the Chatbot

Type any of these to end the conversation:
- `exit`
- `quit`
- `bye`

You'll then see a summary of your emotional journey.

## Output Example

### Final Report

```
======================================================================
          YOUR EMOTIONAL JOURNEY SUMMARY
======================================================================
Final Mood: Positive

Mood Journey: Negative → Positive
• Mood swings: 2
• Peak joy: +0.798 | Peak frustration: -0.456
• Average sentiment: +0.234
• Insight: Amazing recovery! Started negative but ended on a high note.

Messages analyzed: 5
======================================================================
Take care! Come back anytime 💙
```

## Project Structure

```
Chatbot1/
├── chatbot.py              # Main chatbot application
├── test_sentiment.py       # Unit tests for SentimentAnalyzer
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── .env                    # Environment variables (not in version control)
└── .venv/                  # Virtual environment directory
```

## Testing

Run the sentiment analyzer tests:

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

## Sentiment Analysis Details

The chatbot uses **VADER (Valence Aware Dictionary and sEntiment Reasoner)** for sentiment analysis:

- **Positive**: Compound score ≥ 0.05 (😊)
- **Neutral**: Compound score between -0.05 and 0.05 (😐)
- **Negative**: Compound score ≤ -0.05 (😔)

### Mood Tracking Features

- **Mood Swings**: Counts transitions between emotional states
- **Peak Scores**: Tracks the highest positive and lowest negative moments
- **Average Sentiment**: Computes mean emotional tone across the conversation
- **Smart Insights**: Generates context-aware summaries of emotional patterns

## Supported Gemini Models

The chatbot uses `gemini-2.5-flash-lite` by default. Other supported models:

- `gemini-2.5-flash` — Faster, good for quick responses
- `gemini-2.5-pro` — More advanced reasoning
- `gemini-1.5-pro` — Higher quality, slower

To change the model, edit `chatbot.py`:

```python
MODEL_NAME = "gemini-2.5-pro"  # Replace with desired model
```

Check available models: [Google AI Studio - Models](https://aistudio.google.com/app/apikey)

## Configuration

### Adjust Temperature & Token Limit

Edit `chatbot.py` in the `get_response()` method:

```python
generation_config=genai_types.GenerationConfig(
    temperature=0.8,      # Range: 0.0–2.0 (higher = more creative)
    max_output_tokens=600 # Response length limit
)
```

### Customize System Prompt

Edit the `GeminiChatbot.__init__()` method:

```python
system_instruction="You are a warm, empathetic, and caring support assistant. "
                  "Respond with kindness, patience, and understanding."
```

## Troubleshooting

### Error: "GEMINI_API_KEY not found in .env"

**Solution:** Create a `.env` file in the project root and add your API key:
```env
GEMINI_API_KEY=your_key_here
```

### Error: "404 Model not found"

**Solution:** Update `MODEL_NAME` in `chatbot.py` to a valid model:
```python
MODEL_NAME = "gemini-2.5-flash"
```

Visit [Google AI Studio](https://aistudio.google.com/app/apikey) to see available models.

### Error: "Rate limit exceeded"

**Solution:** Wait a few moments before sending the next message, or upgrade your Gemini API plan at [Google AI Studio](https://aistudio.google.com/app/apikey).

### Sentiment Analysis Shows Incorrect Mood

VADER works best with standard English. For improved accuracy:
- Use clear, standard language
- Avoid excessive misspellings
- Contractions are fine (e.g., "I'm happy")

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `google-generativeai` | Latest | Google Gemini API client |
| `vaderSentiment` | Latest | Sentiment analysis |
| `python-dotenv` | Latest | Load environment variables |

## License

This project is open-source and available for personal and educational use.

## Contributing

Feel free to fork, modify, and improve this chatbot! Some ideas:

- Add conversation history persistence (save to JSON/SQLite)
- Implement multi-user support
- Add custom sentiment dictionaries
- Integrate with other LLMs (OpenAI, Claude, etc.)
- Create a web interface (Flask/FastAPI)

## Contact & Support

For issues, questions, or improvements, please open an issue or contact the maintainer.

---

**Happy chatting! 💙**