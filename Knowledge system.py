
import streamlit as st

# Page Config
st.set_page_config(
    page_title="Knowledge System",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>

html, body, [class*="css"] {
    background-color: white;
    color: black;
}

/* Header Box */
.header-box {
    width: 100%;
    background-color: white;
    border: 2px solid black;
    padding: 20px;
    text-align: center;
    font-size: 38px;
    font-weight: bold;
    color: black;
    border-radius: 10px;
    margin-bottom: 20px;
}

/* Main Content Box */
.main-box {
    width: 100%;
    height: 65vh;
    border: 2px solid black;
    border-radius: 10px;
    padding: 20px;
    overflow-y: auto;
    background-color: white;
    color: black;
}

/* Bottom Input Area */
.input-container {
    position: fixed;
    bottom: 20px;
    left: 2%;
    width: 96%;
    background-color: white;
    padding: 10px;
}

.stTextInput > div > div > input {
    background-color: white;
    color: black;
    border: 2px solid black;
    border-radius: 10px;
    padding: 12px;
}

.stButton > button {
    width: 100%;
    height: 50px;
    border-radius: 10px;
    background-color: black;
    color: white;
    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)

# Header
st.markdown(
    '<div class="header-box">Knowledge System</div>',
    unsafe_allow_html=True
)

# Main Full Box
st.markdown(
    '<div class="main-box"></div>',
    unsafe_allow_html=True
)

# Bottom Input Section
st.markdown('<div class="input-container">', unsafe_allow_html=True)

col1, col2 = st.columns([8, 1])

with col1:
    user_input = st.text_input(
        "",
        placeholder="Type your text"
    )

with col2:
    send = st.button("➤")

st.markdown('</div>', unsafe_allow_html=True)

# Optional Output
if send and user_input:
    st.write("You typed:", user_input)
import streamlit as st

# Page Config
st.set_page_config(
    page_title="Knowledge System",
    layout="wide",
)

# ---------------- CSS ----------------
st.markdown("""
<style>

/* পুরো App */
html, body, [class*="css"] {
    font-family: Arial, sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: white;
    width: 270px !important;
    border-right: 1px solid #e5e5e5;
}

/* Sidebar Text */
.sidebar-title {
    font-size: 30px;
    font-weight: bold;
    margin-bottom: 25px;
}

/* Menu Item */
.menu-item {
    font-size: 22px;
    padding: 12px 10px;
    border-radius: 12px;
    margin-bottom: 8px;
    cursor: pointer;
}

.menu-item:hover {
    background-color: #f2f2f2;
}

/* Recent Box */
.recent-box {
    background-color: #f2f2f2;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
    font-size: 18px;
}

/* Main Header */
.main-header {
    font-size: 40px;
    font-weight: bold;
    margin-bottom: 20px;
}

/* Chat Area */
.chat-box {
    height: 72vh;
    border: 1px solid #dddddd;
    border-radius: 15px;
    padding: 20px;
    background-color: white;
    overflow-y: auto;
}

/* Bottom Input */
.stChatInputContainer {
    background-color: white;
}

/* Input */
.stChatInput textarea {
    border-radius: 15px !important;
    border: 1px solid #cccccc !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- Sidebar ----------------
with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">Knowledge System</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="menu-item">✏️ New chat</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu-item">🔍 Search chats</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu-item">📁 Projects</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu-item">⚙️ Codex</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu-item">⋯ More</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### Recents")

    recent_chats = [
        "Streamlit Knowledge System",
        "Color vs Colour",
        "Inline outline symbols",
        "Word Columns Issue Solution",
        "English Medium Conversion",
        "Drawing request",
        "Message Empty Clarification",
        "Photoshop শেখার ভিডিও",
        "CV Format Sources",
        "ল্যাপটপে স্ক্রিনশট নেওয়া"
    ]

    for chat in recent_chats:
        st.markdown(
            f'<div class="recent-box">{chat}</div>',
            unsafe_allow_html=True
        )

# ---------------- Main Area ----------------
st.markdown(
    '<div class="main-header">Knowledge System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="chat-box">'
    '<h3>Welcome 👋</h3>'
    '<p>Your AI Knowledge System is ready.</p>'
    '</div>',
    unsafe_allow_html=True
)

# ---------------- Bottom Chat Input ----------------
prompt = st.chat_input("Type your text")

if prompt:
    st.write(f"🧑 You: {prompt}")
