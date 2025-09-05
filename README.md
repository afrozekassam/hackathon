# Empathetic Journaling App - Terminal MVP

A simple, reliable terminal-based journaling app that helps you reflect on your day with AI-powered insights.

## Features

- **Two modes:**
  - **Make your own entry**: Free-form journaling
  - **Unwind**: Guided session with 5 structured questions
- AI-powered sentiment analysis
- AI-generated personalized reflections
- Fallback template-based reflections when AI is unavailable
- Clean, user-friendly terminal interface
- Interactive menu system

## Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the app:
   ```bash
   python journal.py
   ```

## How it works

1. **Choose your mode:**
   - **Make your own entry**: Write freely about whatever is on your mind
   - **Unwind**: Answer 5 guided questions about your feelings and situation
2. For "Unwind" mode:
   - The app analyzes the sentiment of your responses using Hugging Face AI
   - It generates a personalized reflection using AI (with template fallback)
   - You get a thoughtful, empathetic response to help process your feelings
3. You can continue with more sessions or exit when done

## API Configuration

The app uses Hugging Face's free inference API. You need to set up your API token:

1. Get your own Hugging Face token from https://huggingface.co/settings/tokens
2. Create a `.env` file in the project directory with:
   ```
   HUGGINGFACE_TOKEN=your_token_here
   ```
3. Or set the environment variable directly:
   ```bash
   export HUGGINGFACE_TOKEN=your_token_here
   ```

## Models Used

SENTIMENT_MODEL = "VinMir/GordonAI-emotion_detection"
TEXT_GENERATION_MODEL = "facebook/blenderbot-400M-distill"
## Fallback System

If the AI services are unavailable or timeout, the app automatically falls back to a high-quality template-based reflection system to ensure you always get a meaningful response.
