import streamlit as st
import google.generativeai as genai
import os
import json
import re
from google.api_core.exceptions import GoogleAPIError

# -----------------------------
# Configure Gemini API
# -----------------------------
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-flash-latest")

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
# Session State Setup (for interactive quiz)
# -----------------------------
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None

if "quiz_checked" not in st.session_state:
    st.session_state.quiz_checked = False

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
You are Ashna Study Buddy.

Give one clear, simple, real-world example that helps explain the topic "{topic}".

Keep it beginner-friendly and under 150 words.
Explain briefly why the example fits the topic.
"""

    elif action == "Quiz":

        # Reset previous quiz state since a new quiz is being generated
        st.session_state.quiz_data = None
        st.session_state.quiz_checked = False

        prompt = f"""
Create exactly 5 multiple-choice questions on the topic "{topic}".

Respond with ONLY valid JSON (no markdown, no code fences, no extra text)
in exactly this structure:

{{
  "questions": [
    {{
      "question": "Question text here",
      "options": {{
        "A": "Option A text",
        "B": "Option B text",
        "C": "Option C text",
        "D": "Option D text"
      }},
      "correct": "A",
      "explanation": "Short explanation of why this answer is correct."
    }}
  ]
}}

Generate 5 items in the "questions" list.
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

        if action == "Quiz":

            # Clean up response in case the model wraps it in ```json fences
            raw_text = response.text.strip()
            raw_text = re.sub(r"^```json", "", raw_text).strip()
            raw_text = re.sub(r"^```", "", raw_text).strip()
            raw_text = re.sub(r"```$", "", raw_text).strip()

            try:
                quiz_json = json.loads(raw_text)
                st.session_state.quiz_data = quiz_json.get("questions", [])
                st.session_state.quiz_checked = False
            except json.JSONDecodeError:
                st.error("Couldn't parse the quiz. Please click Quiz again.")

        else:

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


# -----------------------------
# Interactive Quiz Display
# -----------------------------
if st.session_state.quiz_data:

    st.markdown("---")
    st.markdown("## ❓ Quiz")

    user_answers = {}

    for i, q in enumerate(st.session_state.quiz_data):

        st.markdown(f"**Q{i+1}. {q['question']}**")

        option_labels = [f"{key}. {value}" for key, value in q["options"].items()]

        selected = st.radio(
            "Choose an answer:",
            option_labels,
            key=f"quiz_q_{i}",
            index=None,
            label_visibility="collapsed"
        )

        if selected:
            user_answers[i] = selected[0]  # first character is the option letter

        st.write("")

    if st.button("✅ Check Answers"):
        st.session_state.quiz_checked = True
        st.session_state.user_answers = user_answers

    if st.session_state.quiz_checked:

        st.markdown("## 📊 Results")

        score = 0

        for i, q in enumerate(st.session_state.quiz_data):

            picked = st.session_state.user_answers.get(i)
            correct = q["correct"]

            if picked == correct:
                score += 1
                st.markdown(
                    f"""
<div class="response-box">

✅ **Q{i+1}: Correct!**

Your answer: **{picked}**

{q['explanation']}

</div>
""",
                    unsafe_allow_html=True
                )
            else:
                picked_display = picked if picked else "No answer selected"
                st.markdown(
                    f"""
<div class="response-box">

❌ **Q{i+1}: Incorrect**

Your answer: **{picked_display}** | Correct answer: **{correct}**

{q['explanation']}

</div>
""",
                    unsafe_allow_html=True
                )

            st.write("")

        st.markdown(f"### 🏆 Final Score: {score} / {len(st.session_state.quiz_data)}")
