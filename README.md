# 🤖 AI Universe — Django Web App

A **premium dark-themed Django web app** showcasing AI tools like **Gemini, ChatGPT, Claude**, and real-world AI use cases including Music, Video, Images, Code, and more.

## 🚀 Live Pages

| Page | URL | Description |
|------|-----|-------------|
| 🏠 Home | `/` | Hero + 6 AI tool cards (Gemini, ChatGPT, Claude, Midjourney, Suno, Runway) |
| 🎯 Use Cases | `/usecases/` | 8 AI use case categories — Music, Video, Images, Chat, Code, Voice, Writing, Agents |
| 🤖 Explore AI | `/explore/` | AI agent comparison cards + workflow guide + comparison table |

## ✨ Features

- 🌑 **Dark theme** with animated background gradient orbs
- 💎 **Glassmorphism** cards with hover effects
- 🎬 **Scroll animations** — fade-in on scroll
- 📱 **Fully responsive** — with mobile hamburger menu
- 🔤 **Google Fonts** — Outfit + Inter
- 🔗 **Live links** to every AI tool (Gemini, ChatGPT, Suno, Runway, ElevenLabs, etc.)

## 🛠️ Tech Stack

- **Backend:** Django 6.0 (Python)
- **Frontend:** HTML5, Vanilla CSS (no frameworks)
- **Design:** Dark mode, Glassmorphism, CSS animations
- **Database:** SQLite (default)

## ⚙️ Installation & Setup

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/ai-universe-django.git
cd ai-universe-django

# 2. Install dependencies
pip install django

# 3. Run migrations
python manage.py migrate

# 4. Start the server
python manage.py runserver

# 5. Open in browser
# http://127.0.0.1:8000/
```

## 📁 Project Structure

```
Django/
├── manage.py
├── ai_showcase/          # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                 # Main Django app
│   ├── views.py          # Page views with all AI data
│   └── urls.py
├── templates/core/
│   ├── base.html         # Shared nav, footer, scripts
│   ├── home.html         # Page 1 — Home
│   ├── usecases.html     # Page 2 — Use Cases
│   └── explore.html      # Page 3 — Explore AI
└── static/css/style.css  # Full premium dark CSS
```

## 🎨 AI Tools Featured

**Language Models:** Gemini, ChatGPT (GPT-4o), Claude, Perplexity, Grok  
**Image Gen:** Midjourney, DALL·E 3, Stable Diffusion, Adobe Firefly  
**Music Gen:** Suno AI, Udio, MusicLM, Stable Audio  
**Video Gen:** Runway ML, Pika Labs, Sora, Kling AI  
**Voice/Audio:** ElevenLabs, Murf AI, Descript, Whisper  
**Code AI:** GitHub Copilot, Cursor, CodeLlama, Replit  
**AI Agents:** AutoGPT, LangChain, CrewAI, n8n  

---

⭐ **Star this repo** if you found it useful!
