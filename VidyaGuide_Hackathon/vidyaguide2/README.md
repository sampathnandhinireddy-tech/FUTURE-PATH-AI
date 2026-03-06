# ⬡ VidyaGuide — AI Career Planning & Resume Mentor

> Hackathon-ready agentic AI platform for student career planning, resume analysis, and personalised learning guidance.

---

## ⚡ Quick Start (2 options)

### Option A — Open in Browser (Zero Setup)
```
Open frontend/index.html directly in any browser.
All features work instantly in demo mode with intelligent fallback AI.
```

### Option B — Full Stack with Flask (Recommended for Demo)
```bash
cd backend
pip install -r requirements.txt

# Optional: Add Anthropic API key for real Claude AI
cp .env.example .env
# Edit .env → set ANTHROPIC_API_KEY=your_key

python app.py
# Open http://localhost:5000
```

---

## 🏗 Project Structure

```
vidyaguide/
├── frontend/
│   ├── index.html              # Landing page
│   ├── css/style.css           # Liquid glass dark theme
│   ├── js/utils.js             # Shared utilities
│   └── pages/
│       ├── profile.html        # Smart student profile
│       ├── resume.html         # AI resume analyser
│       ├── career.html         # Career roadmap & skills
│       └── agent.html          # AI chat mentor (Vidya)
├── backend/
│   ├── app.py                  # Flask API server
│   ├── requirements.txt
│   └── .env.example
└── README.md
```

---

## ✨ Features

### 📄 Resume Analyser
- ATS Score with animated conic-gradient progress rings
- Keyword analysis: found vs. missing (role-specific)
- Strengths & gap identification
- Priority-ranked improvement suggestions (High/Medium/Low)
- AI-generated bullet point rewrites (before/after)
- Drag & drop file upload + paste text
- Tabbed results interface

### 🧭 Career Roadmap (8 paths)
- Software Engineer, Data Scientist, Product Manager, DevOps, Full-Stack, Data Analyst, UX Designer, Cybersecurity
- Live market data: salary, job openings, growth rate, prep time
- Skill assessment with animated progress bars vs. role benchmarks
- Interactive step-by-step learning roadmap (Done/In Progress/Upcoming)
- Curated resources with Free/Paid labels
- Top 12–14 hiring companies per role

### 🤖 AI Career Agent (Vidya)
- Full Claude API integration with graceful fallback
- Conversation history maintained in session
- Profile-aware context: personalises based on your profile
- Quick action buttons for common queries
- Smart offline responses for: resume, interviews, skills, salary, LinkedIn
- Typing indicator animation
- Export chat as text file

### 👤 Smart Profile
- Comprehensive student profile form
- Skills manager with quick-add and remove
- Persisted to localStorage
- Powers all AI personalisation across the platform

---

## 🔌 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/api/health` | Health check + AI status |
| `POST` | `/api/resume/analyse` | AI resume analysis |
| `GET`  | `/api/career/paths` | All career paths |
| `POST` | `/api/agent/chat` | AI mentor chat |
| `POST` | `/api/skills/assess` | Skill gap analysis |
| `POST` | `/api/profile` | Save profile |

### Resume Analysis Request
```json
{
  "resume_text": "John Doe, Software Engineer...",
  "target_role": "Data Scientist",
  "job_desc": "We are looking for...",
  "profile": { "skills": ["Python", "SQL"] }
}
```

### Agent Chat Request
```json
{
  "messages": [
    { "role": "user", "content": "How should I prepare for Google interviews?" }
  ],
  "profile": { "role": "Software Engineer", "skills": ["Python"] }
}
```

---

## 🎨 Design System

**Theme:** Liquid Glass Dark Minimalism

| Token | Value |
|-------|-------|
| Background | `#070a12` |
| Glass | `rgba(255,255,255,0.048)` |
| Cyan accent | `#5eead4` |
| Blue accent | `#60a5fa` |
| Violet accent | `#c084fc` |
| Font | Outfit (display) + JetBrains Mono (code) |

**Visual effects:**
- Animated ambient orbs with blur (3 orbs, staggered timing)
- Grain texture overlay for depth
- Gradient mesh background layer
- Backdrop-filter glass cards
- Conic-gradient score rings
- CSS transition animations everywhere

---

## 🤖 AI Integration

**With `ANTHROPIC_API_KEY`:**
- Resume analysis → structured JSON from Claude
- Agent chat → real Claude responses with student context
- Model: `claude-sonnet-4-6`

**Without API key (Demo mode):**
- Rule-based resume scoring with realistic outputs
- Smart keyword matching for agent responses
- All UI features work identically

---

## 🛠 Tech Stack

| Layer | Tech |
|-------|------|
| Frontend | HTML5, CSS3 (custom, no frameworks), Vanilla JS |
| Backend | Python Flask + Flask-CORS |
| AI | Anthropic Claude API |
| Storage | localStorage (client-side, session-persistent) |
| Fonts | Google Fonts (Outfit + JetBrains Mono) |
| Deploy | Works on Vercel (frontend) + Railway/Render (backend) |

---

## 🏆 Hackathon Winning Points

1. **Truly agentic** — multi-feature platform, not just a chatbot
2. **Production-grade AI integration** — real Claude API with intelligent fallbacks
3. **India-first design** — salaries in LPA, Indian companies, campus placement focus
4. **Zero external dependencies** — pure HTML/CSS/JS frontend, works offline
5. **Exceptional UX** — liquid glass theme, smooth animations, intuitive flows
6. **Comprehensive** — covers every aspect of student career planning

---

*Built for VidyaGuide Hackathon 2025 · Powered by Anthropic Claude*
