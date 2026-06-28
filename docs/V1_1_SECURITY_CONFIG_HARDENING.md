# SmartEdu AI v1.1.0 Security + Config Hardening

## Scope

This phase hardens local configuration handling and keeps AI provider usage safe by default.

## What changed

- `.env` files remain ignored by Git.
- `.env.example` uses empty placeholders only.
- Backend settings load from the repository root `.env`.
- `AI_PROVIDER` defaults to Groq locally, but invalid values safely fall back to offline mode.
- Numeric AI settings use safe parsing with defaults instead of crashing on bad env values.
- Provider status responses never expose secrets.
- Groq/OpenRouter requests use backend-only keys and fall back to offline if they fail.
- Tests cover missing-key, malformed JSON, and timeout fallback paths.

## Environment setup

Create a local `.env` from `.env.example` and fill only your own values:

```text
AI_PROVIDER=groq
GROQ_API_KEY=
GROQ_MODEL=llama-3.1-8b-instant
OPENROUTER_API_KEY=
OPENROUTER_MODEL=openai/gpt-4o-mini
```

## Safety notes

- Never commit `.env`.
- Never paste real API keys into docs or examples.
- Keep API keys backend-only.
- Use offline mode when provider keys are missing or provider requests fail.

## Verification

The hardening pass is expected to keep these commands working:

- `python -m pytest`
- `python -c "from backend.main import app; print(app.title)"`
- `python -c "from dashboard.config import APP_TITLE; print(APP_TITLE)"`

