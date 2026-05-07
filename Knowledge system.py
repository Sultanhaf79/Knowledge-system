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
    background-color: red ;
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
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: white;
    width: 260px !important;
    border-right: 1px solid #f0f0f0;
}

/* Remove extra padding */
.block-container {
    padding-top: 2rem;
}

/* Menu Items */
.menu-item {
    font-size: 22px;
    color: black;
    margin-bottom: 22px;
    display: flex;
    align-items: center;
    gap: 12px;
}

/* Recents */
.recent-title {
    font-size: 28px;
    font-weight: bold;
    color: black;
    margin-top: 40px;
}

/* Main Area */
.main-title {
    font-size: 42px;
    font-weight: bold;
    color: black;
}

</style>
""", unsafe_allow_html=True)

# ---------------- Sidebar ----------------
with st.sidebar:

    st.markdown(
        '<div class="menu-item">✏️ <span>New chat</span></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="menu-item">🔍 <span>Search chats</span></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="menu-item">⋯ <span>More</span></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="recent-title">Recents</div>',
        unsafe_allow_html=True
    )

# ---------------- Main Page ----------------
st.markdown(
    '<div class="main-title">Knowledge System</div>',
    unsafe_allow_html=True
)

# Chat Input Bottom
prompt = st.chat_input("Type your text")








import streamlit as st

# Page Config
st.set_page_config(
    page_title="Knowledge System",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(to bottom, #f5f5f5, #ececec);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: white;
    width: 260px !important;
    border-right: 1px solid #f0f0f0;
}

/* Menu Items */
.menu-item {
    font-size: 22px;
    color: black;
    margin-bottom: 22px;
    display: flex;
    align-items: center;
    gap: 12px;
}

/* Recents */
.recent-title {
    font-size: 28px;
    font-weight: bold;
    color: black;
    margin-top: 40px;
}

/* Main Title */
.main-title {
    font-size: 42px;
    font-weight: bold;
    color: black;
}

/* Chat Input */
.stChatInput textarea {
    background-color: white !important;
    border-radius: 15px !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- Sidebar ----------------
with st.sidebar:

    st.markdown(
        '<div class="menu-item">✏️ <span>New chat</span></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="menu-item">🔍 <span>Search chats</span></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="menu-item">⋯ <span>More</span></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="recent-title">Recents</div>',
        unsafe_allow_html=True
    )

# ---------------- Main Page ----------------
st.markdown(
    '<div class="main-title">Knowledge System</div>',
    unsafe_allow_html=True
)

# Bottom Input
prompt = st.chat_input("Type your text")



