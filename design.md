# Empathetic Journaling App — Terminal MVP (Design Documentation)

## 1) Problem & Goals
People want to journal consistently but face several challenges:

- **Blank page anxiety** — unsure what to write
- **Difficulty reflecting** — hard to connect entries to meaningful insights
- **Extracting value** — journaling often becomes a log, not a tool for growth

**Goals:**

- Encourage daily journaling with low-friction guided prompts
- Generate personalized, empathetic AI reflections
- Preserve privacy — all data is local, optional export only

---

## 2) Tech Stack
- **Language:** Python 3
- **Libraries:** `requests`, `dotenv`, `json`, `os`
- **Environment Variables:** `.env` for Hugging Face API token (`HUGGINGFACE_TOKEN`)
- **Models / API:**
  - **Sentiment Analysis:** `VinMir/GordonAI-emotion_detection`
  - **Text Generation:** `facebook/blenderbot-400M-distill`
- **Fallback System:** Template-based reflections if AI service is unavailable


---

## 3) Future Enhancements
- On-device AI for offline reflections
- Persistent storage with optional encryption
- **Dynamic follow-up prompts** to track and respond to evolving moods
- Web/GUI version with charts and dashboards
- Voice input: dictation + on-device transcription
- Richer AI models for more nuanced insights
