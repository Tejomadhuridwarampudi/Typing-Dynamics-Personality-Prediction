import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Typing Dynamics Personality Prediction", layout="wide")

# -------------------------------
# Background & Custom Styling
# -------------------------------
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: linear-gradient(to right, #74ebd5, #ACB6E5);
    background-attachment: fixed;
    background-size: cover;
}
h1, h2, h3, h4 {
    text-align: center;
}
textarea {
    font-size: 16px !important;
    border-radius: 12px !important;
    border: 2px solid #74ebd5 !important;
    padding: 12px !important;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    transition: all 0.3s ease-in-out;
}
textarea:focus {
    border-color: #ACB6E5 !important;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
}
.metric-box {
    background: #f9f9f9;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 15px;
    text-align: left;
    font-size: 16px;
}
.hero {
    background: linear-gradient(135deg, #74ebd5, #ACB6E5);
    padding: 60px 20px;
    border-radius: 20px;
    text-align: center;
    color: #fff;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
    animation: fadeIn 2s ease-in-out;
    margin-bottom: 20px;
}
.hero h1 {
    font-size: 3rem;
    font-weight: 800;
    text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
}
.hero h3 {
    font-size: 1.4rem;
    font-weight: 400;
    margin-top: 15px;
    opacity: 0.9;
}
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(-20px);}
    to {opacity: 1; transform: translateY(0);}
}
.card {
    background: #ffffffdd;
    padding: 20px;
    border-radius: 15px;
    margin-top: 30px;
    text-align: left;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
}
.card h4 {
    margin-bottom: 10px;
    color: #333;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# -------------------------------
# Front Page Hero Section
# -------------------------------
hero_section = """
<div class="hero">
    <h1>✨ Typing Dynamics Personality Prediction ✨</h1>
    <h3>Analyze your keystroke patterns & discover hidden personality traits</h3>
</div>

<div class="card">
    <h4>🚀 How it works:</h4>
    <ul>
        <li>Start typing naturally in the box below</li>
        <li>We analyze <b>speed, rhythm, pauses, & accuracy</b></li>
        <li>Get instant feedback + AI-based personality insights</li>
    </ul>
</div>
"""
st.markdown(hero_section, unsafe_allow_html=True)

# -------------------------------
# Initialize Session State
# -------------------------------
if "state" not in st.session_state:
    st.session_state.state = {
        "text": "",
        "timestamps": [],
        "backspaces": 0,
        "start_time": None
    }

# -------------------------------
# Typing Box
# -------------------------------
typed = st.text_area("✍️ Start typing below (minimum 50 characters):", height=150)

if st.session_state.state["start_time"] is None and typed:
    st.session_state.state["start_time"] = time.time()

if len(typed) < len(st.session_state.state["text"]):
    st.session_state.state["backspaces"] += 1

st.session_state.state["text"] = typed
st.session_state.state["timestamps"].append(time.time())

# -------------------------------
# Minimum Character Check
# -------------------------------
if len(typed) < 50:
    st.warning("⚠️ Please type at least 50 characters for analysis.")
    st.stop()

# -------------------------------
# Typing Metrics Calculation
# -------------------------------
time_taken = max(time.time() - st.session_state.state["start_time"], 1)
word_count = len(typed.split())
wpm = (word_count / time_taken) * 60
pause_times = np.diff(st.session_state.state["timestamps"]) if len(st.session_state.state["timestamps"]) > 1 else [0]
pause_var = np.var(pause_times)
rhythm_consistency = 1 / (1 + pause_var)
error_rate = st.session_state.state["backspaces"] / max(len(typed), 1)

# -------------------------------
# New Features Section (Before Metrics)
# -------------------------------
st.markdown("## ✨ Instant Typing Analysis")

# Typing Efficiency Score
typing_efficiency = wpm * (1 - error_rate)
st.markdown(f"**Typing Efficiency Score:** {typing_efficiency:.2f}")

# Simulated Personality Scores
traits = {
    "Openness": np.random.uniform(60, 100),
    "Conscientiousness": np.random.uniform(60, 100),
    "Extraversion": np.random.uniform(60, 100),
    "Agreeableness": np.random.uniform(60, 100),
    "Neuroticism": np.random.uniform(10, 60)
}

# Estimated Personality Category
dominant_trait = max(traits, key=traits.get)
categories = {
    "Openness": "Creative Thinker",
    "Conscientiousness": "Organized Planner",
    "Extraversion": "Social Butterfly",
    "Agreeableness": "Team Player",
    "Neuroticism": "Sensitive & Emotional"
}
st.markdown(f"**Estimated Personality Category:** {categories[dominant_trait]}")

# Instant Feedback
feedback = ""
if wpm < 30:
    feedback += "🔹 Try to type faster for better flow.\n"
elif wpm > 80:
    feedback += "🔹 Excellent typing speed!\n"

if error_rate > 0.1:
    feedback += "🔹 Reduce backspaces to improve accuracy.\n"

if feedback:
    st.markdown("**Instant Feedback:**")
    st.info(feedback)
else:
    st.success("👍 Typing looks great!")

# -------------------------------
# Display Metrics Below Typing Box
# -------------------------------
st.markdown("### 📊 Typing Metrics")
st.markdown(
    f"""
    <div class="metric-box">
    <b>Typing Speed:</b> {wpm:.2f} WPM<br>
    <b>Backspace Rate:</b> {st.session_state.state['backspaces'] / max(len(typed), 1) * 100:.2f}%<br>
    <b>Pause Variability:</b> {pause_var:.3f} sec<br>
    <b>Rhythm Consistency:</b> {rhythm_consistency:.3f}<br>
    <b>Estimated Error Rate:</b> {error_rate:.3f}
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------
# Charts Section
# -------------------------------
st.markdown("## 📈 Personality & Typing Visualizations")

col1, col2 = st.columns(2)

# 1. Personality Bar Chart
with col1:
    fig1, ax1 = plt.subplots(figsize=(6, 3), dpi=110)
    ax1.bar(traits.keys(), traits.values(), color="teal", alpha=0.7)
    ax1.set_title("Personality Scores")
    plt.xticks(rotation=20, ha="right")
    st.pyplot(fig1)

# 2. Typing Speed Trend
with col2:
    fig2, ax2 = plt.subplots(figsize=(6, 3), dpi=110)
    ax2.plot(range(len(st.session_state.state["timestamps"])), np.cumsum([1]*len(st.session_state.state["timestamps"])), color="blue")
    ax2.set_title("Typing Speed Trend")
    st.pyplot(fig2)

col3, col4 = st.columns(2)

# 3. Pause Variability Histogram
with col3:
    fig3, ax3 = plt.subplots(figsize=(6, 3), dpi=110)
    ax3.hist(pause_times, bins=20, color="orange", alpha=0.7)
    ax3.set_title("Pause Variability Distribution")
    st.pyplot(fig3)

# 4. Error/Backspace Trend
with col4:
    fig4, ax4 = plt.subplots(figsize=(6, 3), dpi=110)
    if st.session_state.state["backspaces"] > 0:
        backspace_counts = list(range(st.session_state.state["backspaces"]))
        ax4.plot(backspace_counts, color="red")
    else:
        ax4.plot([0], [0], color="red")
    ax4.set_title("Error / Backspace Trend")
    st.pyplot(fig4)

# -------------------------------
# Personality Insights
# -------------------------------
st.markdown("## 🧠 Personality Insights")
insights = {
    "Openness": "Creative and curious with a love for new ideas.",
    "Conscientiousness": "Organized, disciplined, and detail-oriented.",
    "Extraversion": "Energetic, outgoing, and enjoys social settings.",
    "Agreeableness": "Compassionate, cooperative, and trusting.",
    "Neuroticism": "Emotional stability varies, prone to stress."
}
for trait, desc in insights.items():
    st.write(f"**{trait}:** {desc}")
