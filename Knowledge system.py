
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
    background-color: gray;
    color: darkgray;
}

/* Header Box */
.header-box {
    width: 100%;
    background-color: gray;
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
