import streamlit as st
import os, json, re, base64, requests
from groq import Groq
from docx import Document

st.set_page_config(page_title="AI জ্ঞানভাণ্ডার", page_icon="📚", layout="wide")

GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", "")
GITHUB_REPO  = st.secrets.get("GITHUB_REPO", "")
KB_FILE      = "knowledge_base.json"
GH_API       = "https://api.github.com/repos/" + GITHUB_REPO + "/contents/" + KB_FILE

def load_kb():
    if not GITHUB_TOKEN:
        if os.path.exists(KB_FILE):
            return json.load(open(KB_FILE, encoding="utf-8"))
        return []
    try:
        r = requests.get(GH_API, headers={"Authorization": "token " + GITHUB_TOKEN})
        if r.status_code == 200:
            return json.loads(base64.b64decode(r.json()["content"]).decode("utf-8"))
    except:
        pass
    return []

def search(query, kb, top_k=7):
    if not kb:
        return []
    qw = set(re.findall(r'\w+', query.lower()))
    scored = []
    for c in kb:
        w = set(re.findall(r'\w+', c.get("searchable", "").lower()))
        n = len(qw & w)
        # title exact match হলে বেশি score
        title = str(c.get("cq_num", "")).lower()
        title_match = len(qw & set(re.findall(r'\w+', title)))
        score = n + (title_match * 10)
        if n > 0:
            scored.append((score, c))
            
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in scored[:top_k]]

def get_answer(query, results):
    if not GROQ_API_KEY:
        return "Groq API key missing."
    if not results:
        return "No information found."
    ctx = []
    for i, r in enumerate(results, 1):
        pt = ""
        if r.get("parts"):
            pt = "\n" + "\n".join(k + ". " + v for k, v in r["parts"].items())
        ctx.append("[" + str(i) + "] Book: " + r["book"] + " | " + r["type"] + " | " + str(r["cq_num"]) + "\n" + r["text"][:500] + pt)
    prompt = "You are a knowledge retrieval system. Total items in database: " + str(len([r for r in results])) + " shown out of many. Answer the question using the provided references. Respond in the same language as the question. Always mention book name and item name.\n\nReferences:\n" + "\n\n".join(ctx) + "\n\nQuestion: " + query + "\nAnswer:" Answer the question using the provided references. Respond in the same language as the question. Always mention book name and item name.\n\nReferences:\n" + "\n\n".join(ctx) + "\n\nQuestion: " + query + "\nAnswer:"
    client = Groq(api_key=GROQ_API_KEY)
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=1024
    )
    return resp.choices[0].message.content

# UI

st.markdown("""
<style>
.stDeployButton {display:none;}
#MainMenu {display:none;}
footer {display:none;}
header {display:none;}
[data-testid="stToolbar"] {display:none;}
</style>
""", unsafe_allow_html=True)

st.title("📚 AI জ্ঞানভাণ্ডার")
st.caption("Topic ও CQ নম্বর সহ স্মার্ট সার্চ")

if "kb" not in st.session_state:
    with st.spinner("লোড হচ্ছে..."):
        st.session_state.kb = load_kb()

kb = st.session_state.kb
books = sorted(set(c["book"] for c in kb)) if kb else []

with st.sidebar:
    st.header("📊 ডেটাবেজ তথ্য")
    c1, c2 = st.columns(2)
    c1.metric("বই", len(books))
    c2.metric("আইটেম", len(kb))
    if books:
        st.divider()
        st.subheader("বইয়ের তালিকা")
        for b in books:
            cnt = sum(1 for c in kb if c["book"] == b)
            st.write("📖 " + b + " (" + str(cnt) + ")")

st.divider()
query = st.text_input("🔍 প্রশ্ন লিখুন", placeholder="যেকোনো প্রশ্ন লিখুন...")
if query:
    if not kb:
        st.warning("ডেটাবেজ খালি!")
    else:
        with st.spinner("খোঁজা হচ্ছে..."):
            results = search(query, kb, top_k=7)
            answer = get_answer(query, results)
        st.subheader("📝 উত্তর")
        st.write(answer)
        if results:
            st.divider()
            st.subheader("📄 রেফারেন্স (" + str(len(results)) + "টি উৎস)")
            for i, r in enumerate(results, 1):
                label = "[" + str(i) + "] 📖 " + r["book"] + " | " + str(r["cq_num"])
                with st.expander(label):
                    st.markdown("<h3 style='text-align:center'>" + str(r["cq_num"]) + "</h3>", unsafe_allow_html=True)
                    for line in r["text"].split("\n"):
                        st.write(line)
                    if r.get("parts"):
                        for k, v in r["parts"].items():
                            st.write(k + ". " + v)
else:
    if not kb:
        st.info("বাম দিক থেকে DOCX ফাইল আপলোড করুন।")
    else:
        st.info("উপরে প্রশ্ন লিখুন।")
