# 🖥️ AgentDesk – Autonomous IT Support Agent

An AI-powered system where a user gives a **natural language IT request**, and an AI agent **executes it via browser automation** on a web-based admin panel.

```
User Input → Gemini AI → Structured JSON → Playwright Agent → Browser UI → Task Done
```

## 🏗️ Architecture

| Component | Tech | Purpose |
|-----------|------|---------|
| **Frontend** | Next.js + TailwindCSS + shadcn/ui | Admin panel UI |
| **Backend** | Python + FastAPI | REST API + in-memory storage |
| **AI Parser** | Google Gemini API | Natural language → JSON |
| **Agent** | Python + Playwright | Browser automation |

## 📁 Project Structure

```
agentdesk/
├── frontend/          # Next.js admin panel
│   ├── src/app/
│   │   ├── layout.tsx          # Sidebar navigation
│   │   ├── page.tsx            # Redirect → /users
│   │   ├── users/page.tsx      # Users table + reset buttons
│   │   └── create-user/page.tsx # Create user form
│   └── .env.local              # API URL config
├── backend/
│   ├── main.py                 # FastAPI server
│   └── requirements.txt
├── agent/
│   ├── agent.py                # Playwright browser agent
│   ├── gemini_parser.py        # Gemini AI parser
│   └── requirements.txt
├── .env                        # GEMINI_API_KEY
└── README.md
```

### 🚀 Quick Start (Single Command)

You can start both the backend and frontend simultaneously using the provided starter script:

```bash
./dev.sh
```

### 🛠️ Manual Setup (Step-by-Step)

Backend runs at: `http://localhost:8000`

### 2. Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: `http://localhost:3000`

### 3. Agent Setup

```bash
cd agent
pip install -r requirements.txt
playwright install chromium
```

### 4. Configure API Key

Edit the `.env` file in the project root:
```
GEMINI_API_KEY=your_actual_api_key_here
```

### 5. Run the Agent

```bash
cd agent

# Create a new user
python agent.py "create user john@company.com"

# Reset a password
python agent.py "reset password for jane@company.com"
```

## 🧪 Supported Actions

| Action | Example Input | What the Agent Does |
|--------|--------------|---------------------|
| **Create User** | `"create user alice@company.com"` | Opens `/create-user`, fills email, clicks submit |
| **Reset Password** | `"reset password for john@company.com"` | Opens `/users`, finds user, clicks Reset Password |

## ⚡ API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/users` | List all users |
| `POST` | `/create-user` | Create a new user (`{"email": "..."}`) |
| `POST` | `/reset-password` | Reset user password (`{"email": "..."}`) |

## 🔑 Key Design Decisions

- **Agent uses browser only** – No direct API calls. The agent simulates human interaction via browser automation instead of directly calling backend APIs, demonstrating realistic AI agent behavior.
- **data-testid attributes** – All interactive elements have `data-testid` for reliable Playwright targeting.
- **In-memory storage** – Users are stored in a Python list (resets on server restart).
- **Gemini AI parsing** – Handles messy AI responses with JSON extraction fallbacks.

## 📝 Notes

- Make sure both **frontend** and **backend** are running before starting the agent.
- The agent opens a **visible browser window** so you can watch it work.
- Small delays are added between steps for visual clarity during demos.
