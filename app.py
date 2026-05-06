import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# ==============================
# Load Environment Variables
# ==============================
load_dotenv()

# ==============================
# Groq Client
# ==============================
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ==============================
# Streamlit Page Config
# ==============================
st.set_page_config(
    page_title="AI Code Explainer",
    page_icon="💻",
    layout="wide"
)

# ==============================
# Session State
# ==============================
if "history" not in st.session_state:
    st.session_state.history = []

# ==============================
# Title Section
# ==============================
st.title("💻 AI Code Explainer")
st.write("Explain programming code using AI with bug detection and optimization suggestions.")

# ==============================
# Sidebar Settings
# ==============================
st.sidebar.header("⚙ Settings")

language = st.sidebar.selectbox(
    "Programming Language",
    ["Python", "Java", "JavaScript", "C++", "C"]
)

mode = st.sidebar.radio(
    "Explanation Mode",
    ["Beginner", "Advanced"]
)

model = st.sidebar.selectbox(
    "AI Model",
    [
        "llama-3.1-8b-instant",
        "llama3-70b-8192"
    ]
)

# ==============================
# Main Input Area
# ==============================
code = st.text_area(
    "📌 Paste Your Code Here",
    height=300,
    placeholder="Write or paste your code here..."
)

# ==============================
# Code Preview
# ==============================
if code:
    st.subheader("📄 Code Preview")
    st.code(code, language=language.lower())

# ==============================
# Buttons
# ==============================
col1, col2 = st.columns(2)

with col1:
    explain_button = st.button("🚀 Explain Code")

with col2:
    clear_button = st.button("🗑 Clear History")

# ==============================
# Clear History
# ==============================
if clear_button:
    st.session_state.history = []
    st.success("History Cleared Successfully!")

# ==============================
# Generate Explanation
# ==============================
if explain_button:

    if code.strip() == "":
        st.warning("⚠ Please enter some code.")

    else:

        with st.spinner("Generating AI Explanation..."):

            prompt = f"""
            You are an expert programming tutor and senior software engineer.

            Explain the following {language} code in {mode} mode.

            Your response should include:

            1. What the code does
            2. Step-by-step explanation
            3. Important programming concepts used
            4. Bug detection or bad practices
            5. Code optimization suggestions
            6. Time complexity if applicable
            7. Final summary

            Code:
            {code}
            """

            try:

                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3
                )

                explanation = response.choices[0].message.content

                # ==============================
                # Save History
                # ==============================
                st.session_state.history.append({
                    "language": language,
                    "code": code,
                    "explanation": explanation
                })

                # ==============================
                # Output Tabs
                # ==============================
                tab1, tab2 = st.tabs(
                    ["📘 Explanation", "🐞 Bug Analysis"]
                )

                with tab1:
                    st.subheader("📘 AI Explanation")

                    st.text_area(
                        "Generated Explanation",
                        explanation,
                        height=450
                    )

                with tab2:

                    bug_prompt = f"""
                    Analyze this {language} code for bugs,
                    inefficiencies, and bad coding practices.

                    Code:
                    {code}
                    """

                    bug_response = client.chat.completions.create(
                        model=model,
                        messages=[
                            {
                                "role": "user",
                                "content": bug_prompt
                            }
                        ],
                        temperature=0.2
                    )

                    bug_report = bug_response.choices[0].message.content

                    st.subheader("🐞 Bug Detection Report")

                    st.text_area(
                        "Bug Analysis",
                        bug_report,
                        height=450
                    )

            except Exception as e:
                st.error(f"Error: {e}")

# ==============================
# Previous History
# ==============================
if st.session_state.history:

    st.markdown("---")
    st.subheader("🕘 Previous Explanations")

    for idx, item in enumerate(reversed(st.session_state.history), start=1):

        with st.expander(f"Explanation #{idx}"):

            st.markdown(f"### 🌐 Language: {item['language']}")

            st.code(
                item["code"],
                language=item["language"].lower()
            )

            st.markdown("### 📘 Explanation")

            st.write(item["explanation"])

# ==============================
# Footer
# ==============================
st.markdown("---")

st.caption(
    "🚀 Built with Python, Streamlit, and Groq AI"
)