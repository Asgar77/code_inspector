import streamlit as st
import os
from streamlit_ace import st_ace
from groq import Groq
import time
from streamlit_extras.colored_header import colored_header
from streamlit_extras.switch_page_button import switch_page
from streamlit_option_menu import option_menu
import base64

# Set page configuration
st.set_page_config(
    page_title="Code Inspector Pro",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to enhance the UI
def local_css():
    st.markdown("""
    <style>
    /* Main theme colors and fonts */
    :root {
        --primary-color: #4527a0;
        --secondary-color: #7c4dff;
        --background-color: #f5f5f7;
        --card-background: #ffffff;
        --text-color: #333333;
        --accent-color: #ff5722;
    }
    
    /* Main page styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Custom card styling */
    .card {
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        padding: 1.5rem;
        background-color: var(--card-background);
        margin-bottom: 1rem;
        border-left: 4px solid var(--primary-color);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 6px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Code block styling */
    pre {
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: var(--primary-color);
        font-weight: 700;
    }
    
    /* Custom header with gradient */
    .gradient-header {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: var(--primary-color);
    }
    
    /* Result cards */
    .result-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        border-left: 5px solid var(--secondary-color);
        margin-bottom: 15px;
    }
    
    /* Language icons */
    .language-icon {
        font-size: 24px;
        margin-right: 10px;
        vertical-align: middle;
    }
    
    /* Statistics counter boxes */
    .stat-box {
        background-color: var(--primary-color);
        color: white;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stat-box h3 {
        color: white;
        margin: 0;
        font-size: 28px;
    }
    
    .stat-box p {
        margin: 5px 0 0 0;
        opacity: 0.8;
        font-size: 14px;
    }
    
    /* Toggle switch styling */
    .switch-label {
        display: flex;
        align-items: center;
        cursor: pointer;
        margin: 8px 0;
    }
    
    /* Animation for loading */
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    
    .loading-pulse {
        animation: pulse 1.5s infinite ease-in-out;
    }
    
    /* Main title with fancy gradient */
    .main-title {
        background: linear-gradient(90deg, #4527a0, #7c4dff, #4527a0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 4px 4px 0 0;
        padding: 10px 16px;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--primary-color) !important;
        color: white !important;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-title {
            font-size: 1.8rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# Function to encode image to base64
def get_base64_of_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Function to create HTML for the logo/banner (fallback to text if no image)
def get_logo_html():
    try:
        # If you have a logo image, use this
        # logo_base64 = get_base64_of_image("path/to/logo.png")
        # logo_html = f'<img src="data:image/png;base64,{logo_base64}" alt="Code Inspector Pro Logo" style="width:250px;">'
        # return logo_html
        
        # Fallback to text-based logo with CSS
        return """
        <div style="text-align: center; padding: 20px 0;">
            <h1 class="main-title">Code Inspector Pro</h1>
            <p style="font-size: 1.2rem; color: #666; max-width: 600px; margin: 0 auto;">
                AI-powered code analysis for multiple programming languages
            </p>
        </div>
        """
    except:
        return '<h1 class="main-title">Code Inspector Pro</h1>'

# Display logo/banner
st.markdown(get_logo_html(), unsafe_allow_html=True)

# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "language_stats" not in st.session_state:
    st.session_state.language_stats = {
        "python": 0,
        "javascript": 0,
        "java": 0,
        "csharp": 0,
        "cpp": 0,
        "php": 0,
        "ruby": 0,
        "go": 0,
        "rust": 0,
        "swift": 0,
        "kotlin": 0,
        "typescript": 0
    }
if "code_processed" not in st.session_state:
    st.session_state.code_processed = 0
if "favorite_codes" not in st.session_state:
    st.session_state.favorite_codes = []

# Define available languages with icons
LANGUAGES = {
    "python": "🐍 Python",
    "javascript": "📜 JavaScript",
    "java": "☕ Java",
    "csharp": "🔷 C#",
    "cpp": "⚙️ C++",
    "php": "🐘 PHP",
    "ruby": "💎 Ruby",
    "go": "🔹 Go",
    "rust": "⚡ Rust",
    "swift": "🦅 Swift",
    "kotlin": "🧩 Kotlin",
    "typescript": "🔷 TypeScript"
}

# Language-specific code examples
CODE_EXAMPLES = {
    "python": {
        "Hello World": 'print("Hello, World!")',
        "Fibonacci": "def fibonacci(n):\n    if n <= 0:\n        return []\n    elif n == 1:\n        return [0]\n    elif n == 2:\n        return [0, 1]\n    else:\n        fib = [0, 1]\n        for i in range(2, n):\n            fib.append(fib[i-1] + fib[i-2])\n        return fib\n\nprint(fibonacci(10))",
        "Error Example": "def calculate_average(numbers):\n    total = sum(numbers)\n    return total / len(numbers)\n\nnumbers_list = [10, 20, 30, 40, 0]\nresult = calculate_average(numbers_list)\nprint(f\"The average is: {results}\")"
    },
    "javascript": {
        "Hello World": 'console.log("Hello, World!");',
        "Fibonacci": "function fibonacci(n) {\n    if (n <= 0) return [];\n    if (n === 1) return [0];\n    if (n === 2) return [0, 1];\n    \n    const fib = [0, 1];\n    for (let i = 2; i < n; i++) {\n        fib[i] = fib[i-1] + fib[i-2];\n    }\n    return fib;\n}\n\nconsole.log(fibonacci(10));",
        "Error Example": "function calculateAverage(numbers) {\n    const total = numbers.reduce((sum, num) => sum + num, 0);\n    return total / numbers.length;\n}\n\nconst numbersList = [10, 20, 30, 40, 0];\nconst result = calculateAverage(numbersList);\nconsole.log(`The average is: ${results}`);"
    },
    "java": {
        "Hello World": 'public class HelloWorld {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}',
        "Fibonacci": "import java.util.Arrays;\n\npublic class Fibonacci {\n    public static int[] fibonacci(int n) {\n        if (n <= 0) return new int[0];\n        if (n == 1) return new int[]{0};\n        if (n == 2) return new int[]{0, 1};\n        \n        int[] fib = new int[n];\n        fib[0] = 0;\n        fib[1] = 1;\n        \n        for (int i = 2; i < n; i++) {\n            fib[i] = fib[i-1] + fib[i-2];\n        }\n        \n        return fib;\n    }\n    \n    public static void main(String[] args) {\n        System.out.println(Arrays.toString(fibonacci(10)));\n    }\n}",
        "Error Example": "public class Average {\n    public static double calculateAverage(int[] numbers) {\n        int total = 0;\n        for (int num : numbers) {\n            total += num;\n        }\n        return total / numbers.length;\n    }\n    \n    public static void main(String[] args) {\n        int[] numbersList = {10, 20, 30, 40, 0};\n        double result = calculateAverage(numbersList);\n        System.out.println(\"The average is: \" + results);\n    }\n}"
    },
    "csharp": {
        "Hello World": 'using System;\n\nclass Program {\n    static void Main() {\n        Console.WriteLine("Hello, World!");\n    }\n}',
        "Fibonacci Sequence": "using System;\nusing System.Linq;\n\nclass Program {\n    static int[] Fibonacci(int n) {\n        if (n <= 0) return new int[0];\n        if (n == 1) return new int[] {0};\n        if (n == 2) return new int[] {0, 1};\n        \n        var fib = new int[n];\n        fib[0] = 0;\n        fib[1] = 1;\n        \n        for (int i = 2; i < n; i++) {\n            fib[i] = fib[i-1] + fib[i-2];\n        }\n        \n        return fib;\n    }\n    \n    static void Main() {\n        Console.WriteLine(string.Join(\", \", Fibonacci(10)));\n    }\n}",
        "Error Example": "using System;\n\nclass Program {\n    static double CalculateAverage(int[] numbers) {\n        int total = numbers.Sum();\n        return total / numbers.Length;\n    }\n    \n    static void Main() {\n        int[] numbersList = {10, 20, 30, 40, 0};\n        double result = CalculateAverage(numbersList);\n        Console.WriteLine($\"The average is: {results}\");\n    }\n}"
    },
    "cpp": {
        "Hello World": '#include <iostream>\n\nint main() {\n    std::cout << "Hello, World!" << std::endl;\n    return 0;\n}',
        "Basic Example": "#include <iostream>\n#include <vector>\n\nstd::vector<int> fibonacci(int n) {\n    if (n <= 0) return {};\n    if (n == 1) return {0};\n    if (n == 2) return {0, 1};\n    \n    std::vector<int> fib(n);\n    fib[0] = 0;\n    fib[1] = 1;\n    \n    for (int i = 2; i < n; i++) {\n        fib[i] = fib[i-1] + fib[i-2];\n    }\n    \n    return fib;\n}\n\nint main() {\n    auto fib = fibonacci(10);\n    for (int i = 0; i < fib.size(); i++) {\n        std::cout << fib[i] << \" \";\n    }\n    std::cout << std::endl;\n    return 0;\n}",
        "Error Example": "#include <iostream>\n#include <vector>\n#include <numeric>\n\ndouble calculate_average(const std::vector<int>& numbers) {\n    int total = std::accumulate(numbers.begin(), numbers.end(), 0);\n    return total / numbers.size();\n}\n\nint main() {\n    std::vector<int> numbers_list = {10, 20, 30, 40, 0};\n    double result = calculate_average(numbers_list);\n    std::cout << \"The average is: \" << results << std::endl;\n    return 0;\n}"
    }
}

# Define themes for the code editor
CODE_THEMES = {
    "Dark": "monokai",
    "Light": "github",
    "Solarized": "solarized_dark",
    "Tomorrow": "tomorrow_night",
    "Twilight": "twilight",
    "Dracula": "dracula",
    "Nord": "nord_dark"
}

# Sidebar navigation and configuration
with st.sidebar:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.image("https://img.icons8.com/fluency/96/000000/code.png", width=80)
    st.markdown("# Code Inspector Pro")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Navigation menu
    selected_menu = option_menu(
        "Main Menu", 
        ["Code Editor", "History", "Settings", "About"],
        icons=["code-square", "clock-history", "gear", "info-circle"],
        menu_icon="list", 
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#f0f2f6"},
            "icon": {"color": "orange", "font-size": "20px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#4527a0"},
        }
    )
    
    # Show configuration options when in Code Editor or Settings
    if selected_menu in ["Code Editor", "Settings"]:
        st.markdown("## Configuration")
        
        # API key configuration
        with st.expander("API Settings", expanded=False):
            use_env_var = st.checkbox("Use GROQ_API_KEY environment variable", value=True)
            
            if use_env_var:
                api_key = os.environ.get("GROQ_API_KEY", "")
                if not api_key:
                    st.warning("⚠️ GROQ_API_KEY environment variable not found")
            else:
                api_key = st.text_input("Groq API Key", type="password")
        
        # Model configuration    
        with st.expander("Model Settings", expanded=False):
            # Model selection
            model_option = st.selectbox(
                "Select Model",
                ["llama-3.1-8b", "llama-3.1-70b", "llama-3.1-405b", "llama-3.2-11b", "llama-3.2-82b-online", "llama-3.3-8b-versatile", "llama-3.3-70b-versatile"],
                index=6  # Default to llama-3.3-70b-versatile
            )
            
            # Additional options
            temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
            max_tokens = st.number_input("Max Tokens", 100, 4000, 1000, 100)
        
        # Editor configuration
        with st.expander("Editor Settings", expanded=True):
            theme_option = st.selectbox("Editor Theme", list(CODE_THEMES.keys()))
            font_size = st.slider("Font Size", 10, 24, 14, 1)
            wrap_text = st.checkbox("Wrap Text", value=True)
    
    # Show stats
    if selected_menu != "About":
        st.markdown("## Usage Statistics")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="stat-box">
                <h3>{st.session_state.code_processed}</h3>
                <p>Codes Processed</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            # Find most used language
            most_used = max(st.session_state.language_stats, key=st.session_state.language_stats.get)
            st.markdown(f"""
            <div class="stat-box">
                <h3>{LANGUAGES[most_used].split(' ')[1]}</h3>
                <p>Most Used Language</p>
            </div>
            """, unsafe_allow_html=True)

# Main content
if selected_menu == "Code Editor":
    # Left panel for code input
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        colored_header(label="Code Editor", description="Enter your code below", color_name="violet-70")
        
        # Language selector
        language = st.selectbox("Programming Language", list(LANGUAGES.values()), 
                              format_func=lambda x: x)
        
        # Get language key from selected value
        selected_lang_key = next(key for key, value in LANGUAGES.items() if value == language)
        
        # Example code options for selected language
        lang_examples = CODE_EXAMPLES.get(selected_lang_key, {"None": ""})
        selected_example = st.selectbox("Load Example", list(lang_examples.keys()))
        
        # Initialize code input with example if selected
        initial_code = lang_examples.get(selected_example, "") if selected_example != "None" else ""
        
        # Code editor
        code = st_ace(
            value=initial_code,
            language=selected_lang_key,
            theme=CODE_THEMES[theme_option],
            key="code_input",
            height=400,
            font_size=font_size,
            tab_size=4,
            show_gutter=True,
            show_print_margin=False,
            wrap=wrap_text,
            auto_update=True,
        )
        
        # Action buttons
        btn_cols = st.columns([1, 1, 1, 1])
        with btn_cols[0]:
            review_button = st.button("🔍 Review", use_container_width=True)
        with btn_cols[1]:
            explain_button = st.button("📝 Explain", use_container_width=True)
        with btn_cols[2]:
            optimize_button = st.button("⚡ Optimize", use_container_width=True)
        with btn_cols[3]:
            save_button = st.button("❤️ Save", use_container_width=True)
            
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        colored_header(label="Analysis Results", description="AI-powered code insights", color_name="blue-70")
        
        # Function to process code with Groq
        def process_with_groq(prompt_type, code_snippet, language_key):
            if not api_key:
                st.error("Please provide a Groq API key to continue")
                return None
            
            try:
                client = Groq(api_key=api_key)
                
                # Different system prompts based on action and language
                if prompt_type == "review":
                    system_prompt = f"You are an expert {language_key.upper()} code reviewer. Analyze the code for errors, bugs, and potential improvements. Be specific and concise. Organize your response into sections: 'Issues Found', 'Suggested Fixes', and 'Best Practices'."
                elif prompt_type == "explain":
                    system_prompt = f"You are a {language_key.upper()} tutor explaining code to a student. Break down how the code works line by line, explaining the purpose of each section, functions, and the overall logic. Use simple language and avoid jargon when possible."
                elif prompt_type == "optimize":
                    system_prompt = f"You are a {language_key.upper()} optimization expert. Analyze the code and suggest improvements for performance, readability, and adherence to best practices. Provide optimized code snippets where relevant."
                
                with st.spinner(f"{prompt_type.capitalize()}ing your {language_key} code..."):
                    # Create placeholder for streaming output
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
                    
                    # Process streaming response
                    for chunk in chat_completion:
                        if chunk.choices[0].delta.content is not None:
                            content = chunk.choices[0].delta.content
                            full_response += content
                            result_container.markdown(full_response)
                            time.sleep(0.01)  # Small delay for smoother streaming
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "action": prompt_type,
                        "language": language_key,
                        "code": code_snippet,
                        "response": full_response,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    })
                    
                    # Update language stats
                    st.session_state.language_stats[language_key] = st.session_state.language_stats.get(language_key, 0) + 1
                    
                    # Update total processed count
                    st.session_state.code_processed += 1
                    
                    return full_response
                    
            except Exception as e:
                st.error(f"Error processing request: {str(e)}")
                return None
        
        # Handle button actions
        if code:
            if review_button:
                process_with_groq("review", code, selected_lang_key)
            elif explain_button:
                process_with_groq("explain", code, selected_lang_key)
            elif optimize_button:
                process_with_groq("optimize", code, selected_lang_key)
            elif save_button:
                if code not in [item["code"] for item in st.session_state.favorite_codes]:
                    st.session_state.favorite_codes.append({
                        "language": selected_lang_key,
                        "code": code,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    })
                    st.success("Code saved to favorites!")
                else:
                    st.info("This code is already in your favorites.")
        else:
            st.info("Enter some code and click a button to analyze it.")
        
        st.markdown("</div>", unsafe_allow_html=True)

elif selected_menu == "History":
    colored_header(label="Code History", description="View your previous analyses", color_name="blue-70")
    
    # Tabs for different history views
    tab1, tab2 = st.tabs(["Analysis History", "Favorite Codes"])
    
    with tab1:
        if st.session_state.chat_history:
            for i, item in enumerate(reversed(st.session_state.chat_history)):
                st.markdown(f"""
                <div class="result-card">
                    <h3>{item['action'].capitalize()} - {LANGUAGES.get(item['language'], item['language'])} - {item['timestamp']}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("View Code", expanded=False):
                    st.code(item['code'], language=item['language'])
                
                with st.expander("View Analysis", expanded=False):
                    st.markdown(item['response'])
                
                # Delete button for this history item
                if st.button(f"Delete Entry #{len(st.session_state.chat_history) - i}", key=f"del_hist_{i}"):
                    st.session_state.chat_history.remove(item)
                    st.rerun()
                
                st.markdown("---")
        else:
            st.info("No analysis history yet. Try analyzing some code first!")
    
    with tab2:
        if st.session_state.favorite_codes:
            for i, item in enumerate(reversed(st.session_state.favorite_codes)):
                st.markdown(f"""
                <div class="result-card">
                    <h3>{LANGUAGES.get(item['language'], item['language'])} - {item['timestamp']}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("View Code", expanded=False):
                    st.code(item['code'], language=item['language'])
                
                # Option to run analysis on this saved code
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(f"Review", key=f"review_fav_{i}"):
                        # Redirect to code editor with this code loaded
                        st.session_state.temp_code = item['code']
                        st.session_state.temp_lang = item['language']
                        st.session_state.temp_action = "review"
                        # Would need to implement state management to run this directly
                
                with col2:
                    if st.button(f"Delete", key=f"del_fav_{i}"):
                        st.session_state.favorite_codes.remove(item)
                        st.rerun()
                
                st.markdown("---")
        else:
            st.info("No favorite codes saved yet. Use the ❤️ Save button to add codes to your favorites.")

elif selected_menu == "Settings":
    colored_header(label="Application Settings", description="Customize your experience", color_name="orange-70")
    
    with st.expander("Theme Settings", expanded=True):
        st.markdown("### UI Theme")
        st.radio("Color Theme", ["Light", "Dark", "System Default"], horizontal=True)
        
        st.markdown("### Animations")
        st.checkbox("Enable animations", value=True)
    
    with st.expander("Export/Import Settings", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="Export History",
                data=str(st.session_state.chat_history),
                file_name="code_inspector_history.json",
                mime="application/json",
            )
        with col2:
            st.file_uploader("Import History", type=["json"])
    
    with st.expander("Clear Data", expanded=False):
        st.warning("This will clear all your saved data and cannot be undone.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Clear History"):
                st.session_state.chat_history = []
                st.success("History cleared!")
        with col2:
            if st.button("Clear Favorites"):
                st.session_state.favorite_codes = []
                st.success("Favorites cleared!")
        
        if st.button("Reset All Data", type="primary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.success("All data has been reset!")
            st.rerun()

elif selected_menu == "About":
    colored_header(label="About Code Inspector Pro", description="AI-powered code analysis tool", color_name="green-70")
    
    st.markdown("""
    <div class="card">
        <h2>Code Inspector Pro</h2>
        <p>Version 2.0.0</p>
        
        <h3>Features</h3>
        <ul>
            <li>Multi-language support for Python, JavaScript, Java, C#, C++, PHP, Ruby, Go, Rust, Swift, Kotlin, and TypeScript</li>
            <li>AI-powered code review, explanation, and optimization</li>
            <li>Customizable code editor with multiple themes</li>
            <li>Save favorite code snippets</li>
            <li>Track usage statistics</li>
            <li>Comprehensive history management</li>
        </ul>
        
        <h3>Supported Languages</h3>
        <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 15px;">
            <span class="language-badge" style="background-color: #3572A5; color: white; padding: 5px 10px; border-radius: 10px;">🐍 Python</span>
            <span class="language-badge" style="background-color: #f7df1e; color: black; padding: 5px 10px; border-radius: 10px;">📜 JavaScript</span>
            <span class="language-badge" style="background-color: #b07219; color: white; padding: 5px 10px; border-radius: 10px;">☕ Java</span>
            <span class="language-badge" style="background-color: #178600; color: white; padding: 5px 10px; border-radius: 10px;">🔷 C#</span>
            <span class="language-badge" style="background-color: #f34b7d; color: white; padding: 5px 10px; border-radius: 10px;">⚙️ C++</span>
            <span class="language-badge" style="background-color: #4F5D95; color: white; padding: 5px 10px; border-radius: 10px;">🐘 PHP</span>
            <span class="language-badge" style="background-color: #701516; color: white; padding: 5px 10px; border-radius: 10px;">💎 Ruby</span>
            <span class="language-badge" style="background-color: #00ADD8; color: white; padding: 5px 10px; border-radius: 10px;">🔹 Go</span>
            <span class="language-badge" style="background-color: #dea584; color: black; padding: 5px 10px; border-radius: 10px;">⚡ Rust</span>
            <span class="language-badge" style="background-color: #ffac45; color: black; padding: 5px 10px; border-radius: 10px;">🦅 Swift</span>
            <span class="language-badge" style="background-color: #A97BFF; color: white; padding: 5px 10px; border-radius: 10px;">🧩 Kotlin</span>
            <span class="language-badge" style="background-color: #2b7489; color: white; padding: 5px 10px; border-radius: 10px;">🔷 TypeScript</span>
        </div>
        
        <h3>Powered By</h3>
        <p>This application uses Groq's LLM API for AI-powered code analysis.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add a "Getting Started" section
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## Getting Started")
    
    st.markdown("""
    ### Quick Start Guide
    
    1. **Select a language** from the dropdown menu
    2. **Enter your code** or select an example
    3. **Choose an action**:
       - 🔍 **Review** - Find errors and potential improvements
       - 📝 **Explain** - Get a detailed explanation of how the code works
       - ⚡ **Optimize** - Get suggestions for optimizing performance and readability
       - ❤️ **Save** - Save the code to your favorites for later use
    
    ### Setting Up Your API Key
    
    To use this application, you need a Groq API key:
    
    1. Create an account at [Groq's website](https://console.groq.com)
    2. Generate an API key from your dashboard
    3. Either:
       - Set it as an environment variable `GROQ_API_KEY`
       - Enter it directly in the API Settings panel
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add a FAQ section
    with st.expander("Frequently Asked Questions", expanded=False):
        st.markdown("""
        ### What is Code Inspector Pro?
        
        Code Inspector Pro is an AI-powered tool that helps developers review, understand, and optimize their code across multiple programming languages.
        
        ### How accurate are the AI's suggestions?
        
        The AI provides high-quality suggestions based on best practices, but it's always recommended to review the suggestions before implementing them. The AI's recommendations should be treated as helpful guidance rather than absolute rules.
        
        ### Can I use this for production code?
        
        Yes, but we recommend using it as part of a comprehensive code review process that includes human reviewers as well.
        
        ### Is my code secure?
        
        Your code is processed using Groq's API and is subject to their privacy policy. We do not store your code on our servers except in your local session state.
        
        ### What languages are supported?
        
        Currently, we support Python, JavaScript, Java, C#, C++, PHP, Ruby, Go, Rust, Swift, Kotlin, and TypeScript.
        """)

# Footer
st.markdown("---")
footer_cols = st.columns([3, 1])
with footer_cols[0]:
    st.markdown("💻 **Code Inspector Pro** - Powered by Groq LLM")
with footer_cols[1]:
    st.markdown("© 2025 | v2.0.0")

# Handle state transitions (this would run at the beginning of the next rerun)
if hasattr(st.session_state, 'temp_code') and hasattr(st.session_state, 'temp_lang'):
    # This would set up the editor with the saved code
    # Implementation would depend on Streamlit's state management
    pass