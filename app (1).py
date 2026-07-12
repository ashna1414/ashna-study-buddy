
import streamlit as st
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError

# -----------------------------
# Configure Gemini API
# -----------------------------
genai.configure(api_key="GOOGLE_API_KEY")

model = genai.GenerativeModel("gemini-3.5-flash")

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Ashna Study Buddy",
    page_icon="🎓",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

/* App Background */
.stApp{
    background-color: transparent;
}

/* Main Container */
.block-container{
    max-width:900px;
    padding-top:2rem;
    padding-bottom:2rem;
}

/* Automatically adapt text color */
h1,h2,h3,h4,h5,h6,p,label,span,div{
    color: inherit !important;
}

/* Custom Blue Title */
.title{
    color:#0B3D91 !important;
    text-align:center;
    font-size:48px;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    font-size:22px;
    margin-bottom:25px;
}

/* Textbox */
div.stTextInput input{
    border-radius:12px;
    border:2px solid #0B3D91;
}

/* Buttons */
.stButton > button{
    width:100%;
    height:50px;
    border-radius:12px;
    background:#0B3D91;
    color:white;
    font-size:16px;
    font-weight:bold;
    border:none;
}

.stButton > button:hover{
    background:#2563EB;
    color:white;
}

/* Response Card */
.response-box{
    padding:20px;
    border-radius:15px;
    border-left:6px solid #0B3D91;
    background:rgba(255,255,255,0.10);
    backdrop-filter:blur(10px);
}

/* Hide Footer */
footer{
visibility:hidden;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# Header
# -----------------------------


st.markdown("""
<div class="title">
🎓 Ashna Study Buddy
</div>

<div class="subtitle">
Your Personal AI Learning Assistant 🚀
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Topic
# -----------------------------
topic = st.text_input("📚 Enter Study Topic")

st.write("### Choose an Activity")

col1, col2, col3, col4, col5 = st.columns(5)

action = None

with col1:
    if st.button("📖 Explain"):
        action = "Explain"

with col2:
    if st.button("🌍 Example"):
        action = "Example"

with col3:
    if st.button("❓ Quiz"):
        action = "Quiz"

with col4:
    if st.button("💡 Tips"):
        action = "Tips"

with col5:
    if st.button("🤖 Ask"):
        action = "Ask"


# -----------------------------
# Ask Question Section
# -----------------------------
st.markdown("---")
st.subheader("💬 Ask Anything")

question = st.text_input(
    "Ask a question about the topic above"
)

if st.button("Submit Question"):

    if topic.strip() == "":
        st.warning("Please enter a study topic.")
        st.stop()

    if question.strip() == "":
        st.warning("Please enter your question.")
        st.stop()

    prompt = f"""
You are Ashna Study Buddy.

Study Topic:
{topic}

Student Question:
{question}

Answer only the student's question.

Keep the answer beginner friendly.
Maximum 200 words.
"""

    with st.spinner("Thinking..."):

        response = model.generate_content(prompt)

    st.markdown("## ✨ AI Response")

    st.markdown(
        f"""
<div class="response-box">

{response.text}

</div>
""",
        unsafe_allow_html=True
    )


# -----------------------------
# Prompt Generator
# -----------------------------
if action:

    if topic.strip() == "":
        st.warning("Please enter a study topic.")
        st.stop()

    if action == "Explain":

        prompt = f"""
You are Ashna Study Buddy.

Explain the topic "{topic}" in a simple, beginner-friendly way.

Keep the explanation concise (150-200 words).

Include:
• Definition
• Key Features
• Why it is important
• One simple example

Use bullet points wherever possible.
"""

    elif action == "Example":

        prompt = f"""
Give ONE easy real-life example of {topic}.

Explain it step by step in simple language.
"""

    elif action == "Quiz":

        prompt = f"""
Create 5 multiple-choice questions on {topic}.

Each question should have:

A)
B)
C)
D)

After all questions, provide the correct answer and one-line explanation.
"""

    elif action == "Tips":

        prompt = f"""
Give 8 practical study tips for learning {topic} quickly.

Keep every tip short.
"""

    elif action == "Ask":

        if question.strip() == "":
            st.warning("Please enter your question.")
            st.stop()

        prompt = f"""
You are Ashna Study Buddy.

Study Topic:
{topic}

Student Question:
{question}

Answer ONLY the student's question.

Keep the answer simple, clear, and under 200 words.
"""

    try:

        with st.spinner("Ashna Study Buddy is thinking..."):

            response = model.generate_content(prompt)

        st.markdown("## ✨ AI Response")

        st.markdown(
            f"""
<div class="response-box">

{response.text}

</div>
""",
            unsafe_allow_html=True
        )

    except GoogleAPIError as e:

        st.error(f"Google API Error:\n\n{e}")

    except Exception as e:

        st.error(e)
