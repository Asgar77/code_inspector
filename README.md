# Code Inspector Pro v3.0

AI-powered code analysis for modern developers. Supports code review, explanation, optimization, analytics, history, favorites, and more, with a vibrant, customizable UI.

## 🚀 Features
- Multi-language support (Python, JS, Java, C++, etc.)
- Groq LLM integration for code analysis
- Modern, animated, colorful UI
- Analytics dashboard, history, favorites, and settings

## 🌐 Deploy on Streamlit Cloud

1. **Push this repo to GitHub.**
2. Go to [Streamlit Cloud](https://streamlit.io/cloud) and sign in.
3. Click **New app** and select your repo.
4. Set the main file to `enhanced_code_inspector.py`.
5. Set environment variable `GROQ_API_KEY` in **Settings > Secrets**.
6. Click **Deploy**.

## 📝 Requirements
All dependencies are listed in `requirements.txt`.

## 🛠️ Configuration
- UI theme can be customized in `.streamlit/config.toml`.
- For local run: `streamlit run enhanced_code_inspector.py`

## 📄 License
MIT 