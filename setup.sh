#!/usr/bin/env bash
set -e

echo "🧭 Setting up GitCompass - Open-Source AI Contributor Engine..."
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt

echo "Setup complete! Run:"
echo "  export MODEL_PROVIDER=groq && export GROQ_API_KEY=your_key"
echo "  uvicorn backend.main:app --port 8000"
