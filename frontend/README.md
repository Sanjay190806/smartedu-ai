# SmartEdu AI React Frontend

Production-grade React + TypeScript frontend for SmartEdu AI.

## Stack

- React + TypeScript + Vite
- Tailwind CSS
- Shadcn-style local UI primitives
- Framer Motion
- React Router
- TanStack Query
- Zustand
- Recharts
- Lucide React
- Google OAuth with demo fallback

## Setup

```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```

Default backend:

```text
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Google OAuth is optional:

```text
VITE_GOOGLE_CLIENT_ID=
```

If no Google client ID is configured, use **Continue as Demo Student**.

## Backend

Start FastAPI from the repository root:

```bash
conda activate data
uvicorn backend.main:app --reload
```

Provider API keys for OpenRouter/Groq belong in the backend `.env`, never in this React frontend.
