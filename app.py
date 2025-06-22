import streamlit as st
import os
import json
import time
import base64
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from streamlit_ace import st_ace
from groq import Groq
from streamlit_extras.colored_header import colored_header
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter

# Page Configuration
st.set_page_config(
    page_title="Code Inspector Pro v3.0",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo/code-inspector',
        'Report a bug': 'https://github.com/your-repo/code-inspector/issues',
        'About': 'Code Inspector Pro - AI-powered code analysis tool'
    }
)

# Enhanced CSS with modern design
def load_enhanced_css():
    st.markdown("""
    <style>
    :root {
        --bg-primary: #101010;
        --bg-secondary: #181818;
        --bg-tertiary: #1a1f1a;
        --bg-card: #161d16;
        --bg-input: #181f18;
        --bg-sidebar: #131913;
        --border-primary: #1f3a1f;
        --border-accent: #00ff90;
        --text-primary: #b8ffc8;
        --text-secondary: #6affb7;
        --text-muted: #3e4e3e;
        --text-input: #e0ffe0;
        --btn-primary-bg: #00ff90;
        --btn-primary-text: #101010;
        --btn-secondary-bg: #232d23;
        --btn-secondary-text: #b8ffc8;
        --hover-color: #1e2e1e;
        --active-color: #39ff14;
        --code-keyword: #39ff14;
        --code-string: #00ffea;
        --code-number: #ffb86c;
        --code-func: #00ff90;
        --code-var: #b8ffc8;
        --code-comment: #4e8c4e;
        --code-operator: #00ffea;
        --output-bg: #101510;
        --output-text: #b8ffc8;
        --success-text: #00ff90;
        --warning-text: #ffe066;
        --error-text: #ff4b4b;
        --shadow-glow: 0 0 16px #00ff90, 0 0 2px #39ff14;
        --shadow-card: 0 2px 12px #003f1a44;
        --radius-md: 8px;
        --font-mono: 'Fira Mono', 'SF Mono', 'Consolas', 'Menlo', monospace;
        --font-sans: 'Segoe UI', 'Noto Sans', Arial, sans-serif;
        --transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    body, .main, .block-container {
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        font-family: var(--font-sans) !important;
    }
    h1, h2, h3, h4, h5, h6 {
        color: var(--active-color);
        font-family: var(--font-mono);
        font-weight: 700;
        letter-spacing: 1px;
        text-shadow: 0 0 8px #00ff90cc;
    }
    p, span, div, label {
        color: var(--text-primary) !important;
        font-family: var(--font-sans) !important;
    }
    .enhanced-card, .stat-card, .result-container {
        background: var(--bg-card);
        border: 1.5px solid var(--border-primary);
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-card);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        transition: var(--transition);
        position: relative;
    }
    .enhanced-card:hover, .stat-card:hover, .result-container:hover {
        border-color: var(--border-accent);
        box-shadow: var(--shadow-glow);
        transform: translateY(-2px) scale(1.01);
    }
    .hero-header {
        background: var(--bg-secondary);
        border: 1.5px solid var(--border-accent);
        color: var(--active-color);
        padding: 2.5rem 2rem;
        border-radius: var(--radius-md);
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-glow);
        position: relative;
        font-family: var(--font-mono);
    }
    .hero-header::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #00ff90 0%, #39ff14 100%);
        border-radius: var(--radius-md) var(--radius-md) 0 0;
        box-shadow: 0 0 12px #00ff90cc;
    }
    .stat-number {
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--active-color);
        font-family: var(--font-mono);
        text-shadow: 0 0 8px #00ff9099;
    }
    .stat-label {
        color: var(--text-secondary);
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 500;
    }
    .ace-editor-container {
        border: 1.5px solid var(--border-accent);
        border-radius: var(--radius-md);
        overflow: hidden;
        box-shadow: var(--shadow-glow);
        background: var(--bg-input);
        transition: var(--transition);
    }
    .ace-editor-container:hover {
        border-color: var(--active-color);
        box-shadow: 0 0 16px #00ff90cc;
    }
    .stButton > button {
        background: var(--btn-primary-bg) !important;
        color: var(--btn-primary-text) !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 0.6rem 1.2rem !important;
        font-family: var(--font-mono) !important;
        box-shadow: 0 0 8px #00ff9055;
        transition: var(--transition) !important;
        position: relative;
        overflow: hidden;
        outline: none !important;
    }
    .stButton > button:hover {
        background: var(--active-color) !important;
        color: #101010 !important;
        box-shadow: 0 0 16px #00ff90cc, 0 0 2px #39ff14;
        transform: scale(1.04);
    }
    .stButton > button:active {
        background: #00cc70 !important;
        color: #101010 !important;
        box-shadow: 0 0 8px #00ff90cc;
        transform: scale(0.98);
    }
    .stSelectbox, .stTextInput, .stNumberInput, .stSlider {
        background: var(--bg-input) !important;
        color: var(--text-input) !important;
        border: 1.5px solid var(--border-accent) !important;
        border-radius: var(--radius-md) !important;
        font-family: var(--font-mono) !important;
        font-size: 1.05rem !important;
        transition: var(--transition) !important;
        box-shadow: 0 0 8px #00ff9022;
    }
    .stSelectbox:hover, .stTextInput:hover, .stNumberInput:hover {
        border-color: var(--active-color) !important;
        box-shadow: 0 0 12px #00ff90cc !important;
    }
    .stSelectbox > div > div {
        background: var(--bg-input) !important;
        color: var(--text-input) !important;
    }
    .css-1d391kg, .stSidebar {
        background: var(--bg-sidebar) !important;
        border-right: 2px solid var(--border-accent) !important;
        box-shadow: 0 0 16px #00ff9022;
    }
    pre {
        background: #0d120d !important;
        border: 1.5px solid var(--border-accent) !important;
        border-radius: var(--radius-md) !important;
        color: var(--code-var) !important;
        font-family: var(--font-mono) !important;
        padding: 1rem !important;
        overflow-x: auto !important;
        font-size: 1.05rem !important;
        box-shadow: 0 0 8px #00ff9022;
    }
    code {
        background: #101510 !important;
        color: var(--code-var) !important;
        font-family: var(--font-mono) !important;
        border: 1px solid var(--border-accent) !important;
        padding: 0.25rem 0.5rem !important;
        border-radius: 4px !important;
        font-size: 1rem !important;
        transition: var(--transition) !important;
    }
    code:hover {
        border-color: var(--active-color) !important;
        background: #181f18 !important;
    }
    .notification {
        padding: 1rem;
        border-radius: var(--radius-md);
        margin: 1rem 0;
        border-left: 4px solid var(--border-accent);
        font-family: var(--font-sans);
        background: var(--bg-card);
        border: 1.5px solid var(--border-accent);
        color: var(--active-color);
        box-shadow: 0 0 8px #00ff9022;
        transition: var(--transition);
    }
    .notification.success { border-left-color: var(--success-text); color: var(--success-text); }
    .notification.warning { border-left-color: var(--warning-text); color: var(--warning-text); }
    .notification.error { border-left-color: var(--error-text); color: var(--error-text); }
    .notification.info { border-left-color: var(--active-color); color: var(--active-color); }
    ::-webkit-scrollbar {
        width: 8px; height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary); border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb {
        background: var(--border-accent); border-radius: 4px; transition: var(--transition);
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--active-color);
    }
    .stProgress > div > div > div {
        background: var(--active-color) !important;
        box-shadow: 0 0 8px #00ff90cc;
    }
    .streamlit-expanderHeader {
        background: var(--bg-card) !important;
        color: var(--active-color) !important;
        border: 1.5px solid var(--border-accent) !important;
        border-radius: var(--radius-md) !important;
        font-family: var(--font-mono) !important;
        font-weight: 700 !important;
        transition: var(--transition) !important;
        text-shadow: 0 0 8px #00ff90cc;
    }
    .streamlit-expanderHeader:hover {
        border-color: var(--active-color) !important;
        background: var(--hover-color) !important;
    }
    .streamlit-expanderContent {
        background: var(--bg-card) !important;
        border: 1.5px solid var(--border-accent) !important;
        border-top: none !important;
        border-radius: 0 0 var(--radius-md) var(--radius-md) !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-card) !important;
        border-bottom: 1.5px solid var(--border-accent) !important;
        border-radius: var(--radius-md) var(--radius-md) 0 0 !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: var(--bg-card) !important;
        color: var(--text-secondary) !important;
        border: 1.5px solid var(--border-accent) !important;
        border-bottom: none !important;
        font-family: var(--font-mono) !important;
        font-weight: 600 !important;
        transition: var(--transition) !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--active-color) !important;
        background: var(--hover-color) !important;
    }
    .stTabs [aria-selected="true"] {
        background: var(--active-color) !important;
        color: #101010 !important;
        border-color: var(--active-color) !important;
        text-shadow: 0 0 8px #00ff90cc;
    }
    .stMetric {
        background: var(--bg-card) !important;
        border: 1.5px solid var(--border-accent) !important;
        border-radius: var(--radius-md) !important;
        padding: 1rem !important;
        transition: var(--transition) !important;
        color: var(--active-color) !important;
        font-family: var(--font-mono) !important;
    }
    .stMetric > div > div > div {
        color: var(--active-color) !important;
        font-family: var(--font-mono) !important;
        font-weight: 700 !important;
    }
    .stMetric > div > div > div:last-child {
        color: var(--text-secondary) !important;
        font-family: var(--font-sans) !important;
        font-size: 0.95rem !important;
    }
    .language-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background: #101510;
        color: var(--active-color);
        border: 1.5px solid var(--border-accent);
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        font-family: var(--font-mono);
        transition: var(--transition);
        box-shadow: 0 0 8px #00ff9022;
    }
    .language-badge:hover {
        border-color: var(--active-color);
        background: #181f18;
        color: #39ff14;
    }
    .action-buttons {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 0.75rem;
        margin-top: 1rem;
    }
    .separator {
        height: 1px;
        background: var(--border-accent);
        margin: 1.5rem 0;
        box-shadow: 0 0 8px #00ff9022;
    }
    .status-indicator {
        display: inline-block;
        width: 8px; height: 8px;
        border-radius: 50%;
        margin-right: 0.5rem;
    }
    .status-indicator.success { background: var(--success-text); }
    .status-indicator.warning { background: var(--warning-text); }
    .status-indicator.error { background: var(--error-text); }
    .status-indicator.info { background: var(--active-color); }
    .code-keyword { color: var(--code-keyword) !important; }
    .code-string { color: var(--code-string) !important; }
    .code-number { color: var(--code-number) !important; }
    .code-func { color: var(--code-func) !important; }
    .code-var { color: var(--code-var) !important; }
    .code-comment { color: var(--code-comment) !important; }
    .code-operator { color: var(--code-operator) !important; }
    ::selection {
        background: var(--active-color);
        color: #101010;
    }
    /* Animations */
    @keyframes glow {
        0% { box-shadow: 0 0 8px #00ff90cc; }
        50% { box-shadow: 0 0 24px #00ff90cc, 0 0 8px #39ff14; }
        100% { box-shadow: 0 0 8px #00ff90cc; }
    }
    .enhanced-card, .stat-card, .result-container, .stButton > button:hover {
        animation: glow 2.5s infinite alternate;
    }
    .loading-spinner {
        display: inline-block;
        width: 24px; height: 24px;
        border: 3px solid #232d23;
        border-radius: 50%;
        border-top-color: var(--active-color);
        animation: spin 1s linear infinite;
    }
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    /* Matrix-style background (optional, subtle) */
    body::before {
        content: '';
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        pointer-events: none;
        z-index: 0;
        background: repeating-linear-gradient(
            to bottom,
            rgba(0,255,144,0.04) 0px,
            rgba(0,255,144,0.08) 2px,
            transparent 4px, transparent 32px
        );
        opacity: 0.7;
        animation: matrix-bg 8s linear infinite;
    }
    @keyframes matrix-bg {
        0% { background-position-y: 0; }
        100% { background-position-y: 32px; }
    }
    </style>
    """, unsafe_allow_html=True)

# Data structures
@dataclass
class CodeAnalysis:
    action: str
    language: str
    code: str
    response: str
    timestamp: str
    execution_time: float
    model_used: str
    tokens_used: Optional[int] = None

@dataclass
class FavoriteCode:
    language: str
    code: str
    timestamp: str
    description: str
    tags: List[str]

# Configuration class
class Config:
    LANGUAGES = {
        "python": {"name": "🐍 Python", "color": "#3572A5", "extensions": [".py"]},
        "javascript": {"name": "📜 JavaScript", "color": "#f7df1e", "extensions": [".js", ".jsx"]},
        "java": {"name": "☕ Java", "color": "#b07219", "extensions": [".java"]},
        "csharp": {"name": "🔷 C#", "color": "#178600", "extensions": [".cs"]},
        "cpp": {"name": "⚙️ C++", "color": "#f34b7d", "extensions": [".cpp", ".cc", ".cxx"]},
        "php": {"name": "🐘 PHP", "color": "#4F5D95", "extensions": [".php"]},
        "ruby": {"name": "💎 Ruby", "color": "#701516", "extensions": [".rb"]},
        "go": {"name": "🔹 Go", "color": "#00ADD8", "extensions": [".go"]},
        "rust": {"name": "⚡ Rust", "color": "#dea584", "extensions": [".rs"]},
        "swift": {"name": "🦅 Swift", "color": "#ffac45", "extensions": [".swift"]},
        "kotlin": {"name": "🧩 Kotlin", "color": "#A97BFF", "extensions": [".kt"]},
        "typescript": {"name": "🔷 TypeScript", "color": "#2b7489", "extensions": [".ts", ".tsx"]}
    }
    
    CODE_THEMES = {
        "Dark": "monokai",
        "Light": "github",
        "Solarized": "solarized_dark",
        "Tomorrow": "tomorrow_night",
        "Twilight": "twilight",
        "Dracula": "dracula",
        "Nord": "nord_dark",
        "Material": "material",
        "Oceanic": "oceanic_next"
    }
    
    GROQ_MODELS = {
        "llama-3.1-8b": {"name": "Llama 3.1 8B", "speed": "Fast", "quality": "Good"},
        "llama-3.1-70b": {"name": "Llama 3.1 70B", "speed": "Medium", "quality": "Excellent"},
        "llama-3.1-405b": {"name": "Llama 3.1 405B", "speed": "Slow", "quality": "Best"},
        "llama-3.2-11b": {"name": "Llama 3.2 11B", "speed": "Fast", "quality": "Very Good"},
        "llama-3.2-82b-online": {"name": "Llama 3.2 82B Online", "speed": "Medium", "quality": "Excellent"},
        "llama-3.3-8b-versatile": {"name": "Llama 3.3 8B Versatile", "speed": "Fast", "quality": "Good"},
        "llama-3.3-70b-versatile": {"name": "Llama 3.3 70B Versatile", "speed": "Medium", "quality": "Excellent"}
    }

# Initialize session state
def initialize_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "language_stats" not in st.session_state:
        st.session_state.language_stats = {lang: 0 for lang in Config.LANGUAGES.keys()}
    if "code_processed" not in st.session_state:
        st.session_state.code_processed = 0
    if "favorite_codes" not in st.session_state:
        st.session_state.favorite_codes = []
    if "user_preferences" not in st.session_state:
        st.session_state.user_preferences = {
            "theme": "Dark",
            "font_size": 14,
            "wrap_text": True,
            "auto_save": True,
            "notifications": True
        }
    if "api_usage" not in st.session_state:
        st.session_state.api_usage = {
            "total_requests": 0,
            "total_tokens": 0,
            "total_cost": 0.0
        }

# Enhanced utility functions
def create_notification(message: str, type: str = "info"):
    """Create a styled notification"""
    st.markdown(f"""
    <div class="notification {type}">
        {message}
    </div>
    """, unsafe_allow_html=True)

def format_execution_time(seconds: float) -> str:
    """Format execution time in a human-readable format"""
    if seconds < 1:
        return f"{seconds * 1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    else:
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds:.1f}s"

def estimate_tokens(text: str) -> int:
    """Rough estimation of tokens (4 characters per token)"""
    return len(text) // 4

def calculate_cost(tokens: int, model: str) -> float:
    """Calculate estimated cost based on tokens and model"""
    # Groq pricing (approximate)
    pricing = {
        "llama-3.1-8b": 0.05 / 1000000,  # $0.05 per 1M tokens
        "llama-3.1-70b": 0.59 / 1000000,  # $0.59 per 1M tokens
        "llama-3.1-405b": 2.39 / 1000000,  # $2.39 per 1M tokens
        "llama-3.2-11b": 0.10 / 1000000,  # $0.10 per 1M tokens
        "llama-3.2-82b-online": 0.59 / 1000000,  # $0.59 per 1M tokens
        "llama-3.3-8b-versatile": 0.05 / 1000000,  # $0.05 per 1M tokens
        "llama-3.3-70b-versatile": 0.59 / 1000000,  # $0.59 per 1M tokens
    }
    return tokens * pricing.get(model, 0.05 / 1000000)

# Enhanced AI processing function
def process_with_groq(prompt_type: str, code_snippet: str, language_key: str, 
                     api_key: str, model_option: str, temperature: float, 
                     max_tokens: int) -> Optional[CodeAnalysis]:
    """Enhanced AI processing with better error handling and metrics"""
    
    if not api_key:
        create_notification("Please provide a Groq API key to continue", "error")
        return None
    
    start_time = time.time()
    
    try:
        client = Groq(api_key=api_key)
        
        # Enhanced system prompts
        system_prompts = {
            "review": f"""You are an expert {language_key.upper()} code reviewer with 10+ years of experience.
Analyze the code for:
1. **Syntax Errors**: Identify any syntax issues
2. **Logic Errors**: Find logical problems and edge cases
3. **Performance Issues**: Suggest optimizations
4. **Security Vulnerabilities**: Identify potential security risks
5. **Best Practices**: Recommend improvements for maintainability
6. **Code Quality**: Assess readability and structure

Format your response with clear sections and use markdown formatting.""",
            
            "explain": f"""You are a senior {language_key.upper()} developer explaining code to a junior developer.
Provide a comprehensive explanation including:
1. **Overview**: What the code does at a high level
2. **Line-by-line Analysis**: Explain each important section
3. **Key Concepts**: Highlight important programming concepts used
4. **Flow Diagram**: Describe the execution flow
5. **Common Pitfalls**: What to watch out for
6. **Learning Resources**: Suggest further reading

Use simple language and provide examples where helpful.""",
            
            "optimize": f"""You are a {language_key.upper()} performance optimization expert.
Analyze the code and provide:
1. **Performance Analysis**: Identify bottlenecks and inefficiencies
2. **Optimization Suggestions**: Specific improvements with code examples
3. **Memory Usage**: Analyze memory consumption patterns
4. **Time Complexity**: Assess algorithmic efficiency
5. **Alternative Approaches**: Suggest different solutions
6. **Benchmarking Tips**: How to measure improvements

Provide before/after code comparisons where relevant."""
        }
        
        system_prompt = system_prompts.get(prompt_type, system_prompts["review"])
        
        with st.spinner(f"🤖 {prompt_type.capitalize()}ing your {language_key} code..."):
            result_container = st.empty()
            full_response = ""
            
            # Make API call
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Here's the {language_key} code to {prompt_type}:\n\n```{language_key}\n{code_snippet}\n```"}
                ],
                model=model_option,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            # Process streaming response with progress
            progress_bar = st.progress(0)
            for i, chunk in enumerate(chat_completion):
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    result_container.markdown(full_response)
                    progress_bar.progress(min((i + 1) / 100, 1.0))
                    time.sleep(0.01)
            
            progress_bar.empty()
            
            # Calculate metrics
            execution_time = time.time() - start_time
            estimated_tokens = estimate_tokens(full_response + code_snippet)
            estimated_cost = calculate_cost(estimated_tokens, model_option)
            
            # Create analysis object
            analysis = CodeAnalysis(
                action=prompt_type,
                language=language_key,
                code=code_snippet,
                response=full_response,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                execution_time=execution_time,
                model_used=model_option,
                tokens_used=estimated_tokens
            )
            
            # Update session state
            st.session_state.chat_history.append(asdict(analysis))
            st.session_state.language_stats[language_key] += 1
            st.session_state.code_processed += 1
            st.session_state.api_usage["total_requests"] += 1
            st.session_state.api_usage["total_tokens"] += estimated_tokens
            st.session_state.api_usage["total_cost"] += estimated_cost
            
            # Show success notification
            create_notification(
                f"✅ Analysis completed in {format_execution_time(execution_time)} | "
                f"Tokens: {estimated_tokens:,} | "
                f"Cost: ${estimated_cost:.4f}",
                "success"
            )
            
            return analysis
            
    except Exception as e:
        execution_time = time.time() - start_time
        create_notification(f"❌ Error processing request: {str(e)}", "error")
        return None

# Main application
def main():
    # Load enhanced CSS
    load_enhanced_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Initialize configuration variables with defaults
    api_key = ""
    model_option = "llama-3.3-70b-versatile"
    temperature = 0.7
    max_tokens = 1000
    theme_option = "Dark"
    font_size = 14
    wrap_text = True
    
    # Hero header
    st.markdown("""
    <div class="hero-header">
        <h1>🚀 Code Inspector Pro</h1>
        <p>AI-powered code analysis for modern developers</p>
        <div style="margin-top: 1rem;">
            <span style="background: rgba(0, 122, 204, 0.1); padding: 0.5rem 1rem; border-radius: 20px; margin: 0 0.5rem; border: 1px solid var(--active-color); color: var(--active-color); font-weight: 500;">
                v3.0 VS Code Edition
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown('<div class="enhanced-card">', unsafe_allow_html=True)
        st.image("https://img.icons8.com/fluency/96/000000/code.png", width=80)
        st.markdown("## Code Inspector Pro")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Navigation menu
        selected_menu = option_menu(
            "Main Menu", 
            ["Code Editor", "Dashboard", "History", "Settings", "About"],
            icons=["code-square", "bar-chart", "clock-history", "gear", "info-circle"],
            menu_icon="list", 
            default_index=0,
            styles={
                "container": {"padding": "5px", "background-color": "var(--bg-card)", "border": "1px solid var(--border-primary)", "border-radius": "var(--radius-sm)"},
                "icon": {"color": "var(--active-color)", "font-size": "20px"}, 
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "var(--hover-color)", "color": "var(--text-primary)", "font-family": "var(--font-sans)", "border-radius": "var(--radius-sm)", "padding": "8px 12px"},
                "nav-link-selected": {"background-color": "var(--active-color)", "color": "white"},
            }
        )
        
        # Configuration panel
        if selected_menu in ["Code Editor", "Settings"]:
            st.markdown("## ⚙️ Configuration")
            
            # API Settings
            with st.expander("🔑 API Settings", expanded=False):
                use_env_var = st.checkbox("Use GROQ_API_KEY environment variable", value=True)
                
                if use_env_var:
                    api_key = os.environ.get("GROQ_API_KEY", "")
                    if not api_key:
                        st.warning("⚠️ GROQ_API_KEY environment variable not found")
                else:
                    api_key = st.text_input("Groq API Key", type="password")
            
            # Model Settings
            with st.expander("🤖 Model Settings", expanded=False):
                model_option = st.selectbox(
                    "Select Model",
                    list(Config.GROQ_MODELS.keys()),
                    format_func=lambda x: f"{Config.GROQ_MODELS[x]['name']} ({Config.GROQ_MODELS[x]['speed']})",
                    index=6
                )
                
                # Show model info
                model_info = Config.GROQ_MODELS[model_option]
                st.info(f"**{model_info['name']}** - Speed: {model_info['speed']}, Quality: {model_info['quality']}")
                
                temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
                max_tokens = st.number_input("Max Tokens", 100, 4000, 1000, 100)
            
            # Editor Settings
            with st.expander("📝 Editor Settings", expanded=True):
                theme_option = st.selectbox("Editor Theme", list(Config.CODE_THEMES.keys()))
                font_size = st.slider("Font Size", 10, 24, 14, 1)
                wrap_text = st.checkbox("Wrap Text", value=True)
        
        # Statistics
        if selected_menu != "About":
            st.markdown("## 📊 Quick Stats")
            
            # Create statistics cards
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{st.session_state.code_processed}</div>
                    <div class="stat-label">Codes Processed</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                most_used = max(st.session_state.language_stats, key=st.session_state.language_stats.get)
                most_used_name = Config.LANGUAGES[most_used]['name'].split(' ')[1]  # Get just the language name without emoji
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{most_used_name}</div>
                    <div class="stat-label">Most Used</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Main content routing
    if selected_menu == "Code Editor":
        render_code_editor(api_key, model_option, temperature, max_tokens, theme_option, font_size, wrap_text)
    elif selected_menu == "Dashboard":
        render_dashboard()
    elif selected_menu == "History":
        render_history()
    elif selected_menu == "Settings":
        render_settings()
    elif selected_menu == "About":
        render_about()

def render_code_editor(api_key, model_option, temperature, max_tokens, theme_option, font_size, wrap_text):
    """Render the enhanced code editor interface"""
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown('<div class="enhanced-card">', unsafe_allow_html=True)
        colored_header(label="📝 Code Editor", description="Write or paste your code below", color_name="violet-70")
        
        # Language selector with enhanced UI
        language_options = [lang_info["name"] for lang_info in Config.LANGUAGES.values()]
        language = st.selectbox(
            "Programming Language", 
            language_options
        )
        
        # Get language key
        selected_lang_key = next(key for key, value in Config.LANGUAGES.items() if value["name"] == language)
        
        # Code examples
        lang_examples = get_code_examples(selected_lang_key)
        selected_example = st.selectbox("Load Example", ["None"] + list(lang_examples.keys()))
        
        # Initialize code
        initial_code = lang_examples.get(selected_example, "") if selected_example != "None" else ""
        
        # Enhanced code editor
        st.markdown('<div class="ace-editor-container">', unsafe_allow_html=True)
        code = st_ace(
            value=initial_code,
            language=selected_lang_key,
            theme=Config.CODE_THEMES[theme_option],
            key="code_input",
            height=400,
            font_size=font_size,
            tab_size=4,
            show_gutter=True,
            show_print_margin=False,
            wrap=wrap_text,
            auto_update=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Action buttons with enhanced styling
        st.markdown("### Actions")
        btn_cols = st.columns([1, 1, 1, 1])
        
        with btn_cols[0]:
            review_button = st.button("🔍 Review", use_container_width=True, type="primary")
        with btn_cols[1]:
            explain_button = st.button("📝 Explain", use_container_width=True)
        with btn_cols[2]:
            optimize_button = st.button("⚡ Optimize", use_container_width=True)
        with btn_cols[3]:
            save_button = st.button("❤️ Save", use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="enhanced-card">', unsafe_allow_html=True)
        colored_header(label="🤖 Analysis Results", description="AI-powered insights", color_name="blue-70")
        
        # Handle button actions
        if code:
            if review_button:
                process_with_groq("review", code, selected_lang_key, api_key, model_option, temperature, max_tokens)
            elif explain_button:
                process_with_groq("explain", code, selected_lang_key, api_key, model_option, temperature, max_tokens)
            elif optimize_button:
                process_with_groq("optimize", code, selected_lang_key, api_key, model_option, temperature, max_tokens)
            elif save_button:
                save_favorite_code(code, selected_lang_key)
        else:
            st.info("💡 Enter some code and click an action button to analyze it.")
        
        st.markdown("</div>", unsafe_allow_html=True)

def get_code_examples(language: str) -> Dict[str, str]:
    """Get code examples for a specific language"""
    examples = {
        "python": {
            "Hello World": 'print("Hello, World!")',
            "Fibonacci": """def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    else:
        fib = [0, 1]
        for i in range(2, n):
            fib.append(fib[i-1] + fib[i-2])
        return fib

print(fibonacci(10))""",
            "Error Example": """def calculate_average(numbers):
    total = sum(numbers)
    return total / len(numbers)

numbers_list = [10, 20, 30, 40, 0]
result = calculate_average(numbers_list)
print(f"The average is: {results}")""",
            "Async Example": """import asyncio
import aiohttp

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    urls = ['https://api.github.com/users/1', 'https://api.github.com/users/2']
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

asyncio.run(main())"""
        },
        "javascript": {
            "Hello World": 'console.log("Hello, World!");',
            "Fibonacci": """function fibonacci(n) {
    if (n <= 0) return [];
    if (n === 1) return [0];
    if (n === 2) return [0, 1];
    
    const fib = [0, 1];
    for (let i = 2; i < n; i++) {
        fib[i] = fib[i-1] + fib[i-2];
    }
    return fib;
}

console.log(fibonacci(10));""",
            "Error Example": """function calculateAverage(numbers) {
    const total = numbers.reduce((sum, num) => sum + num, 0);
    return total / numbers.length;
}

const numbersList = [10, 20, 30, 40, 0];
const result = calculateAverage(numbersList);
console.log(`The average is: ${results}`);""",
            "Async Example": """async function fetchData(url) {
    const response = await fetch(url);
    return await response.text();
}

async function main() {
    const urls = ['https://api.github.com/users/1', 'https://api.github.com/users/2'];
    const promises = urls.map(url => fetchData(url));
    const results = await Promise.all(promises);
    return results;
}

main().then(console.log);"""
        },
        "java": {
            "Hello World": """public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}""",
            "Fibonacci": """import java.util.Arrays;

public class Fibonacci {
    public static int[] fibonacci(int n) {
        if (n <= 0) return new int[0];
        if (n == 1) return new int[]{0};
        if (n == 2) return new int[]{0, 1};
        
        int[] fib = new int[n];
        fib[0] = 0;
        fib[1] = 1;
        
        for (int i = 2; i < n; i++) {
            fib[i] = fib[i-1] + fib[i-2];
        }
        
        return fib;
    }
    
    public static void main(String[] args) {
        System.out.println(Arrays.toString(fibonacci(10)));
    }
}""",
            "Error Example": """public class Average {
    public static double calculateAverage(int[] numbers) {
        int total = 0;
        for (int num : numbers) {
            total += num;
        }
        return total / numbers.length;
    }
    
    public static void main(String[] args) {
        int[] numbersList = {10, 20, 30, 40, 0};
        double result = calculateAverage(numbersList);
        System.out.println("The average is: " + results);
    }
}"""
        },
        "csharp": {
            "Hello World": """using System;

class Program {
    static void Main() {
        Console.WriteLine("Hello, World!");
    }
}""",
            "Fibonacci": """using System;
using System.Linq;

class Program {
    static int[] Fibonacci(int n) {
        if (n <= 0) return new int[0];
        if (n == 1) return new int[] {0};
        if (n == 2) return new int[] {0, 1};
        
        var fib = new int[n];
        fib[0] = 0;
        fib[1] = 1;
        
        for (int i = 2; i < n; i++) {
            fib[i] = fib[i-1] + fib[i-2];
        }
        
        return fib;
    }
    
    static void Main() {
        Console.WriteLine(string.Join(", ", Fibonacci(10)));
    }
}""",
            "Error Example": """using System;

class Program {
    static double CalculateAverage(int[] numbers) {
        int total = numbers.Sum();
        return total / numbers.Length;
    }
    
    static void Main() {
        int[] numbersList = {10, 20, 30, 40, 0};
        double result = CalculateAverage(numbersList);
        Console.WriteLine($"The average is: {results}");
    }
}"""
        },
        "cpp": {
            "Hello World": """#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}""",
            "Fibonacci": """#include <iostream>
#include <vector>

std::vector<int> fibonacci(int n) {
    if (n <= 0) return {};
    if (n == 1) return {0};
    if (n == 2) return {0, 1};
    
    std::vector<int> fib(n);
    fib[0] = 0;
    fib[1] = 1;
    
    for (int i = 2; i < n; i++) {
        fib[i] = fib[i-1] + fib[i-2];
    }
    
    return fib;
}

int main() {
    auto fib = fibonacci(10);
    for (int i = 0; i < fib.size(); i++) {
        std::cout << fib[i] << " ";
    }
    std::cout << std::endl;
    return 0;
}""",
            "Error Example": """#include <iostream>
#include <vector>
#include <numeric>

double calculate_average(const std::vector<int>& numbers) {
    int total = std::accumulate(numbers.begin(), numbers.end(), 0);
    return total / numbers.size();
}

int main() {
    std::vector<int> numbers_list = {10, 20, 30, 40, 0};
    double result = calculate_average(numbers_list);
    std::cout << "The average is: " << results << std::endl;
    return 0;
}"""
        }
    }
    
    # Default examples for other languages
    default_examples = {
        "Hello World": f"// {language} Hello World example",
        "Basic Example": f"// {language} basic code example",
        "Error Example": f"// {language} code with potential errors"
    }
    
    return examples.get(language, default_examples)

def save_favorite_code(code: str, language: str):
    """Save code to favorites with description and tags"""
    if code not in [item["code"] for item in st.session_state.favorite_codes]:
        # Create a simple dialog for description
        description = st.text_input("Add a description (optional):", key="fav_desc")
        tags = st.text_input("Add tags (comma-separated):", key="fav_tags")
        
        if st.button("Save to Favorites"):
            favorite = FavoriteCode(
                language=language,
                code=code,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                description=description or "No description",
                tags=tags.split(",") if tags else []
            )
            st.session_state.favorite_codes.append(asdict(favorite))
            create_notification("✅ Code saved to favorites!", "success")
            st.rerun()
    else:
        create_notification("ℹ️ This code is already in your favorites.", "info")

def render_dashboard():
    """Render the analytics dashboard"""
    st.markdown('<div class="enhanced-card">', unsafe_allow_html=True)
    colored_header(label="📊 Analytics Dashboard", description="Your coding insights and statistics", color_name="blue-70")
    
    # Overview statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{st.session_state.code_processed}</div>
            <div class="stat-label">Total Analyses</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{st.session_state.api_usage['total_requests']}</div>
            <div class="stat-label">API Requests</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{st.session_state.api_usage['total_tokens']:,}</div>
            <div class="stat-label">Tokens Used</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">${st.session_state.api_usage['total_cost']:.4f}</div>
            <div class="stat-label">Total Cost</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Charts and visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="enhanced-card">', unsafe_allow_html=True)
        st.markdown("### Language Usage")
        
        # Create language usage chart
        languages = list(st.session_state.language_stats.keys())
        counts = list(st.session_state.language_stats.values())
        
        if sum(counts) > 0:
            fig = px.pie(
                values=counts,
                names=[Config.LANGUAGES[lang]["name"] for lang in languages],
                title="Code Analysis by Language"
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#f0f6fc')
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available yet. Start analyzing code to see statistics!")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="enhanced-card">', unsafe_allow_html=True)
        st.markdown("### Analysis Types")
        
        # Create analysis type chart
        if st.session_state.chat_history:
            analysis_types = [item["action"] for item in st.session_state.chat_history]
            type_counts = Counter(analysis_types)
            
            fig = px.bar(
                x=list(type_counts.keys()),
                y=list(type_counts.values()),
                title="Analysis Types Used",
                labels={"x": "Analysis Type", "y": "Count"}
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#f0f6fc')
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No analysis history yet!")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Recent activity
    st.markdown('<div class="enhanced-card">', unsafe_allow_html=True)
    st.markdown("### Recent Activity")
    
    if st.session_state.chat_history:
        recent_analyses = st.session_state.chat_history[-5:]  # Last 5 analyses
        
        for analysis in reversed(recent_analyses):
            with st.expander(f"{analysis['action'].capitalize()} - {Config.LANGUAGES[analysis['language']]['name']} - {analysis['timestamp']}", expanded=False):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.code(analysis['code'][:200] + "..." if len(analysis['code']) > 200 else analysis['code'], language=analysis['language'])
                with col2:
                    st.metric("Execution Time", format_execution_time(analysis['execution_time']))
                    st.metric("Tokens Used", f"{analysis['tokens_used']:,}")
    else:
        st.info("No recent activity. Start analyzing code to see your history!")
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_history():
    """Render the enhanced history interface"""
    st.markdown('<div class="enhanced-card">', unsafe_allow_html=True)
    colored_header(label="📚 Analysis History", description="View and manage your previous analyses", color_name="blue-70")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        language_options = ["All"] + [lang_info["name"] for lang_info in Config.LANGUAGES.values()]
        filter_language = st.selectbox("Filter by Language", language_options)
    with col2:
        filter_action = st.selectbox("Filter by Action", ["All", "review", "explain", "optimize"])
    with col3:
        search_term = st.text_input("Search in code or responses", placeholder="Enter search term...")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Tabs for different views
    tab1, tab2 = st.tabs(["📊 Analysis History", "❤️ Favorite Codes"])
    
    with tab1:
        if st.session_state.chat_history:
            # Filter history based on selections
            filtered_history = st.session_state.chat_history
            
            if filter_language != "All":
                # Get the language key from the selected language name
                selected_lang_key = next(key for key, value in Config.LANGUAGES.items() if value["name"] == filter_language)
                filtered_history = [item for item in filtered_history if item["language"] == selected_lang_key]
            
            if filter_action != "All":
                filtered_history = [item for item in filtered_history if item["action"] == filter_action]
            
            if search_term:
                filtered_history = [
                    item for item in filtered_history 
                    if search_term.lower() in item["code"].lower() or search_term.lower() in item["response"].lower()
                ]
            
            if filtered_history:
                for i, item in enumerate(filtered_history):
                    st.markdown(f"""
                    <div class="result-container">
                        <h3>{item['action'].capitalize()} - {Config.LANGUAGES[item['language']]['name']} - {item['timestamp']}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Metrics row
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Execution Time", format_execution_time(item['execution_time']))
                    with col2:
                        st.metric("Tokens Used", f"{item['tokens_used']:,}")
                    with col3:
                        st.metric("Model", item['model_used'])
                    with col4:
                        st.metric("Code Length", f"{len(item['code'])} chars")
                    
                    # Code and analysis
                    col1, col2 = st.columns(2)
                    with col1:
                        with st.expander("View Code", expanded=False):
                            st.code(item['code'], language=item['language'])
                    with col2:
                        with st.expander("View Analysis", expanded=False):
                            st.markdown(item['response'])
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button(f"🔄 Re-run", key=f"rerun_{i}"):
                            st.session_state.temp_code = item['code']
                            st.session_state.temp_lang = item['language']
                            st.session_state.temp_action = item['action']
                            st.rerun()
                    with col2:
                        if st.button(f"❤️ Save", key=f"save_{i}"):
                            save_favorite_code(item['code'], item['language'])
                    with col3:
                        if st.button(f"🗑️ Delete", key=f"delete_{i}"):
                            st.session_state.chat_history.remove(item)
                            st.rerun()
                    
                    st.markdown("---")
            else:
                st.info("No analyses match your current filters.")
        else:
            st.info("No analysis history yet. Try analyzing some code first!")
    
    with tab2:
        if st.session_state.favorite_codes:
            for i, item in enumerate(st.session_state.favorite_codes):
                st.markdown(f"""
                <div class="result-container">
                    <h3>{Config.LANGUAGES[item['language']]['name']} - {item['timestamp']}</h3>
                    <p><strong>Description:</strong> {item['description']}</p>
                    {f"<p><strong>Tags:</strong> {', '.join(item['tags'])}</p>" if item['tags'] else ""}
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("View Code", expanded=False):
                    st.code(item['code'], language=item['language'])
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(f"🔍 Review", key=f"review_fav_{i}"):
                        st.session_state.temp_code = item['code']
                        st.session_state.temp_lang = item['language']
                        st.session_state.temp_action = "review"
                        st.rerun()
                with col2:
                    if st.button(f"📝 Explain", key=f"explain_fav_{i}"):
                        st.session_state.temp_code = item['code']
                        st.session_state.temp_lang = item['language']
                        st.session_state.temp_action = "explain"
                        st.rerun()
                with col3:
                    if st.button(f"🗑️ Delete", key=f"del_fav_{i}"):
                        st.session_state.favorite_codes.remove(item)
                        st.rerun()
                
                st.markdown("---")
        else:
            st.info("No favorite codes saved yet. Use the ❤️ Save button to add codes to your favorites.")

def render_settings():
    """Render the enhanced settings interface"""
    st.markdown('<div class="enhanced-card">', unsafe_allow_html=True)
    colored_header(label="⚙️ Application Settings", description="Customize your experience", color_name="orange-70")
    
    # Theme Settings
    with st.expander("🎨 Theme Settings", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### UI Theme")
            theme_mode = st.radio("Color Theme", ["Light", "Dark", "System Default"], horizontal=True)
            
            st.markdown("### Animations")
            enable_animations = st.checkbox("Enable animations", value=True)
            
            st.markdown("### Notifications")
            enable_notifications = st.checkbox("Show notifications", value=True)
        
        with col2:
            st.markdown("### Auto-save")
            auto_save = st.checkbox("Auto-save code changes", value=True)
            
            st.markdown("### Code Editor")
            show_line_numbers = st.checkbox("Show line numbers", value=True)
            show_minimap = st.checkbox("Show minimap", value=False)
    
    # Export/Import Settings
    with st.expander("📁 Export/Import Settings", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Export Data")
            if st.button("📤 Export History"):
                history_data = json.dumps(st.session_state.chat_history, indent=2)
                st.download_button(
                    label="Download History JSON",
                    data=history_data,
                    file_name=f"code_inspector_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                )
            
            if st.button("📤 Export Favorites"):
                favorites_data = json.dumps(st.session_state.favorite_codes, indent=2)
                st.download_button(
                    label="Download Favorites JSON",
                    data=favorites_data,
                    file_name=f"code_inspector_favorites_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                )
        
        with col2:
            st.markdown("### Import Data")
            uploaded_history = st.file_uploader("Import History", type=["json"])
            if uploaded_history:
                try:
                    history_data = json.load(uploaded_history)
                    if st.button("Import History"):
                        st.session_state.chat_history = history_data
                        create_notification("✅ History imported successfully!", "success")
                except:
                    create_notification("❌ Invalid JSON file", "error")
    
    # Data Management
    with st.expander("🗑️ Data Management", expanded=False):
        st.warning("⚠️ These actions will clear your data and cannot be undone.")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Clear History", type="secondary"):
                st.session_state.chat_history = []
                create_notification("✅ History cleared!", "success")
        
        with col2:
            if st.button("Clear Favorites", type="secondary"):
                st.session_state.favorite_codes = []
                create_notification("✅ Favorites cleared!", "success")
        
        with col3:
            if st.button("Reset All Data", type="primary"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                initialize_session_state()
                create_notification("✅ All data has been reset!", "success")
                st.rerun()
    
    # API Usage Statistics
    with st.expander("📊 API Usage Statistics", expanded=False):
        st.markdown("### Usage Overview")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Requests", st.session_state.api_usage["total_requests"])
        with col2:
            st.metric("Total Tokens", f"{st.session_state.api_usage['total_tokens']:,}")
        with col3:
            st.metric("Total Cost", f"${st.session_state.api_usage['total_cost']:.4f}")
        
        # Cost breakdown by model
        if st.session_state.chat_history:
            st.markdown("### Cost Breakdown by Model")
            model_costs = {}
            for item in st.session_state.chat_history:
                model = item['model_used']
                cost = calculate_cost(item['tokens_used'], model)
                model_costs[model] = model_costs.get(model, 0) + cost
            
            for model, cost in model_costs.items():
                st.metric(model, f"${cost:.4f}")
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_about():
    """Render the enhanced about page"""
    st.markdown('<div class="enhanced-card">', unsafe_allow_html=True)
    colored_header(label="ℹ️ About Code Inspector Pro", description="AI-powered code analysis tool", color_name="green-70")
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2>🚀 Code Inspector Pro v3.0</h2>
        <p style="font-size: 1.1rem; color: var(--text-secondary);">
            The next generation of AI-powered code analysis
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features grid
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✨ Key Features")
        features = [
            "🤖 **AI-Powered Analysis**: Advanced code review, explanation, and optimization",
            "🌍 **Multi-Language Support**: 12+ programming languages",
            "📊 **Analytics Dashboard**: Comprehensive usage statistics and insights",
            "💾 **Smart History**: Searchable analysis history with filters",
            "❤️ **Favorites System**: Save and organize your favorite code snippets",
            "⚙️ **Customizable**: Themes, settings, and preferences",
            "📱 **Responsive Design**: Works on desktop, tablet, and mobile",
            "🔒 **Privacy First**: Your code stays on your device"
        ]
        
        for feature in features:
            st.markdown(f"• {feature}")
    
    with col2:
        st.markdown("### 🛠️ Supported Languages")
        
        # Language grid
        languages_grid = []
        for lang_key, lang_info in Config.LANGUAGES.items():
            languages_grid.append(f"""
            <div style="display: inline-block; margin: 5px; padding: 8px 12px; 
                        background: {lang_info['color']}20; border: 1px solid {lang_info['color']}40; 
                        border-radius: 6px; font-size: 0.9rem; font-family: 'Courier New', monospace;">
                {lang_info['name']}
            </div>
            """)
        
        st.markdown("".join(languages_grid), unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Getting Started
    st.markdown('<div class="enhanced-card">', unsafe_allow_html=True)
    st.markdown("## 🚀 Getting Started")
    
    st.markdown("""
    ### Quick Start Guide
    
    1. **🔑 Set up your API key** in the Settings panel
    2. **📝 Select a language** from the dropdown menu
    3. **💻 Enter your code** or choose an example
    4. **🤖 Choose an action**:
       - 🔍 **Review** - Find errors and improvements
       - 📝 **Explain** - Get detailed explanations
       - ⚡ **Optimize** - Performance suggestions
       - ❤️ **Save** - Add to favorites
    
    ### 🎯 Best Practices
    
    - Start with small code snippets for faster analysis
    - Use specific examples to get better AI responses
    - Review AI suggestions before implementing
    - Save useful code snippets for future reference
    """)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # FAQ Section
    with st.expander("❓ Frequently Asked Questions", expanded=False):
        st.markdown("""
        ### 🤔 What is Code Inspector Pro?
        
        Code Inspector Pro is an AI-powered tool that helps developers review, understand, and optimize their code across multiple programming languages using advanced language models.
        
        ### 🎯 How accurate are the AI suggestions?
        
        The AI provides high-quality suggestions based on best practices and common patterns. However, always review suggestions before implementing them in production code.
        
        ### 🔒 Is my code secure?
        
        Yes! Your code is processed using Groq's API and is subject to their privacy policy. We do not store your code on our servers - everything is kept in your local session.
        
        ### 💰 How much does it cost?
        
        The application itself is free. You only pay for the Groq API usage, which is very affordable (typically less than $0.01 per analysis).
        
        ### 🆘 Need help?
        
        Check out our documentation or create an issue on GitHub for support.
        """)
    
    # Footer
    st.markdown("---")
    footer_cols = st.columns([3, 1])
    with footer_cols[0]:
        st.markdown("💻 **Code Inspector Pro v3.0 VS Code Edition** - Powered by Groq LLM")
    with footer_cols[1]:
        st.markdown("© 2025 | VS Code Edition")

if __name__ == "__main__":
    main() 
