# SmartEdu AI

SmartEdu AI is an AI-powered academic intelligence and career mentoring platform for students.

It combines machine learning academic risk prediction, explainable recommendations, a FastAPI backend, an AI Mentor interview engine, a Streamlit backup dashboard, and a premium React + TypeScript frontend.

> SmartEdu AI is a guidance tool. Predictions are probabilistic and should not replace human mentors, teachers, academic counselors, or institutional decision-making.

## Features

- ML academic risk prediction.
- Explainable risk factors.
- FastAPI backend.
- SQLite local persistence.
- Student CRUD.
- Batch CSV prediction.
- Analytics endpoints and dashboard views.
- Personalized recommendation engine.
- AI Mentor adaptive interview.
- Offline mentor fallback.
- Optional OpenRouter/Groq provider support.
- Streamlit backup dashboard under `dashboard/`.
- React + TypeScript premium frontend under `frontend/`.
- Demo auth and optional Google OAuth.
- Light and dark theme.
- Mentor report downloads as JSON, Markdown, and TXT.

## Architecture

```text
React frontend -> FastAPI backend -> ML model + AI mentor engine -> SQLite database
```

The Streamlit dashboard remains available as a backup interface.

## Phase Status

| Phase | Scope | Status |
| --- | --- | --- |
| Phase 1 | ML Foundation | Complete |
| Phase 2 | FastAPI Backend | Complete |
| Phase 3 | Streamlit Dashboard Backup | Complete |
| Phase 4 | AI Mentor Intelligence Engine | Complete |
| Phase 5 | React Frontend | Complete |
| Phase 5.5 | Premium UI Polish | Planned |
| Phase 6 | Deployment + Production Auth | Planned |

## Folder Structure

```text
backend/     FastAPI app, database, routes, schemas, services, AI provider adapters
dashboard/   Streamlit backup dashboard
frontend/    React + TypeScript + Vite frontend
ml/          ML preprocessing, training, evaluation, prediction, artifacts
data/        Sample data generation and synthetic CSV
tests/       Pytest coverage for ML/backend/dashboard helpers/mentor engine
docs/        Project reports and supporting documentation
```

## Backend Setup

```bash
conda activate data
pip install -r requirements.txt
python data/generate_sample_data.py
python ml/train_model.py
uvicorn backend.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

## React Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

React frontend URL:

```text
http://127.0.0.1:5173
```

Build check:

```bash
cd frontend
npm run build
```

## Streamlit Backup Dashboard

```bash
streamlit run dashboard/app.py
```

Streamlit URL:

```text
http://localhost:8501
```

## Tests

Backend and Python tests:

```bash
python -m pytest
```

Frontend production build:

```bash
cd frontend
npm run build
```

## Environment Variables

Create a backend `.env` from `.env.example` when needed.

```text
DATABASE_URL=sqlite:///./smartedu.db
MODEL_PATH=ml/model_registry/model.joblib
PREPROCESSOR_PATH=ml/model_registry/preprocessor.joblib
APP_ENV=development
AI_PROVIDER=offline
OPENROUTER_API_KEY=
OPENROUTER_MODEL=openai/gpt-4o-mini
GROQ_API_KEY=
GROQ_MODEL=llama-3.1-8b-instant
AI_REQUEST_TIMEOUT=30
AI_MAX_TOKENS=1800
AI_TEMPERATURE=0.4
```

Create a frontend `frontend/.env` from `frontend/.env.example` when needed.

```text
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_GOOGLE_CLIENT_ID=
```

Never commit `.env` files or real API keys.

## AI Provider Configuration

Default local mode:

```text
AI_PROVIDER=offline
```

OpenRouter:

```text
AI_PROVIDER=openrouter
OPENROUTER_API_KEY=your_key
OPENROUTER_MODEL=openai/gpt-4o-mini
```

Groq:

```text
AI_PROVIDER=groq
GROQ_API_KEY=your_key
GROQ_MODEL=llama-3.1-8b-instant
```

If a hosted provider is missing a key or fails, the backend falls back to the offline mentor engine. Provider status never exposes API keys.

## Demo Flow

1. Start the FastAPI backend.
2. Start the React frontend.
3. Continue as Demo Student.
4. Open Overview.
5. Run Risk Prediction.
6. Start AI Mentor interview.
7. Generate Mentor Report.
8. Download report.
9. Open Analytics/System pages.

## React Frontend Routes

| Route | Purpose |
| --- | --- |
| `/` | Premium landing page |
| `/login` | Google OAuth or demo mode login |
| `/about` | Project explanation |
| `/privacy` | Privacy and AI disclaimer |
| `/app/overview` | Main dashboard overview |
| `/app/predict` | Risk prediction form and report |
| `/app/students` | Student table and profile view |
| `/app/batch` | CSV batch prediction workflow |
| `/app/mentor` | Adaptive AI Mentor interview |
| `/app/report/:sessionId` | Human-readable mentor report |
| `/app/analytics` | Risk and subject analytics |
| `/app/system` | Backend/provider/system status |
| `/app/settings` | Theme, auth, API URL, and security notes |

## Safety And Ethics

SmartEdu AI should be used as a support tool. It can help mentors identify students who may need support, explain model signals, and generate guidance plans. It should not be used as a final judgment about a student's ability, future, mental health, or academic standing.

## Known Limitations

- Google auth is frontend-local demo auth, not production backend auth.
- SQLite is local-first, not a production database.
- Dataset is synthetic.
- AI provider keys are optional and backend-only.
- Streamlit remains backup.
- Deployment is not done yet.
- Premium UI polish is planned.

## Git Hygiene

Do not commit:

- `.env`
- `frontend/.env`
- `smartedu.db`
- `*.db`
- `frontend/node_modules/`
- `frontend/dist/`
- `__pycache__/`
- `.pytest_cache/`
- virtual environment folders
