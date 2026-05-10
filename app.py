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

def save_kb(data):
    content = base64.b64encode(json.dumps(data, ensure_ascii=False, indent=2).encode()).decode()
    headers = {"Authorization": "token " + GITHUB_TOKEN}
    sha = None
    r = requests.get(GH_API, headers=headers)
    if r.status_code == 200:
        sha = r.json()["sha"]
    payload = {"message": "update kb", "content": content}
    if sha:
        payload["sha"] = sha
    requests.put(GH_API, headers=headers, json=payload)

def parse_docx(file_bytes, book_name):
    import io
    doc = Document(io.BytesIO(file_bytes))
    chunks = []
    paras = doc.paragraphs

    content_type = "CQ"
    for p in paras[:5]:
        m = re.search(r'Type\s*[:\-]\s*(\w+)', p.text.strip(), re.IGNORECASE)
        if m:
            content_type = m.group(1).upper()
            break

    if content_type == "CQ":
        cur_topic = "General"
        cur_cq = None
        cur_lines = []
        cur_parts = {}
        cur_part = None

        def flush_cq():
            if cur_cq and cur_lines:
                full = "\n".join(cur_lines)
                chunks.append({
                    "book": book_name,
                    "type": "CQ",
                    "topic": cur_topic,
                    "cq_num": cur_cq,
                    "text": full,
                    "parts": dict(cur_parts),
                    "searchable": book_name + " CQ " + cur_topic + " " + full + " " + " ".join(cur_parts.values())
                })

        for p in paras:
            t = p.text.strip()
            if not t or re.search(r'Type\s*[:\-]\s*\w+', t, re.IGNORECASE):
                continue
            tm = re.search(r'Topic\s*[-]?\s*(\d+)', t, re.IGNORECASE)
            if tm:
                flush_cq()
                cur_topic = "Topic-" + tm.group(1)
                cur_cq = None
                cur_lines = []
                cur_parts = {}
                cur_part = None
                continue
            cm = re.match(r'^([১২৩৪৫৬৭৮৯০1-9]\d*)[।.]', t)
            if cm:
                flush_cq()
                cur_cq = cm.group(1)
                cur_lines = [t]
                cur_parts = {}
                cur_part = None
                continue
            pm = re.match(r'^([কখগঘ])[।.]\s*(.*)', t)
            if pm:
                cur_part = pm.group(1)
                cur_parts[cur_part] = pm.group(2)
                if cur_lines:
                    cur_lines.append(t)
                continue
            if cur_cq:
                if cur_part and cur_part in cur_parts:
                    cur_parts[cur_part] += " " + t
                cur_lines.append(t)
        flush_cq()

    elif content_type == "MCQ":
        cur_q = None
        cur_lines = []
        cur_opts = {}

        def flush_mcq():
            if cur_q and cur_lines:
                full = "\n".join(cur_lines)
                chunks.append({
                    "book": book_name,
                    "type": "MCQ",
                    "topic": "MCQ",
                    "cq_num": cur_q,
                    "text": full,
                    "parts": dict(cur_opts),
                    "searchable": book_name + " MCQ " + full + " " + " ".join(cur_opts.values())
                })

        for p in paras:
            t = p.text.strip()
            if not t or re.search(r'Type\s*[:\-]\s*\w+', t, re.IGNORECASE):
                continue
            qm = re.match(r'^([১২৩৪৫৬৭৮৯০1-9]\d*)[।.]', t)
            if qm:
                flush_mcq()
                cur_q = qm.group(1)
                cur_lines = [t]
                cur_opts = {}
                continue
            om = re.match(r'^[\(\[]?([কখগঘABCDabcd])[)\]।.]\s*(.*)', t)
            if om and cur_q:
                cur_opts[om.group(1)] = om.group(2)
                cur_lines.append(t)
                continue
            am = re.search(r'উত্তর\s*[:\-।]?\s*(.*)', t)
            if am and cur_q:
                cur_opts["Ans"] = am.group(1)
                cur_lines.append(t)
                continue
            if cur_q:
                cur_lines.append(t)
        flush_mcq()

    else:
        cur_title = None
        cur_lines = []
        started = False

        def flush_item():
            if cur_lines and cur_title:
                full = "\n".join(cur_lines)
                chunks.append({
                    "book": book_name,
                    "type": content_type,
                    "topic": content_type,
                    "cq_num": cur_title,
                    "text": full,
                    "parts": {},
                    "searchable": book_name + " " + content_type + " " + cur_title + " " + cur_title + " " + cur_title + " " + full
                })

        for p in paras:
            t = p.text.strip()
            if not t or re.search(r'Type\s*[:\-]\s*\w+', t, re.IGNORECASE):
                continue
            is_bold = p.runs and any(run.bold for run in p.runs if run.text.strip())
            is_num = re.match(r'^(\d+|[১২৩৪৫৬৭৮৯০]+)[।.]\s+.{5,}', t)
            if is_bold and is_num:
                flush_item()
                started = True
                cur_title = re.sub(r'^(\d+|[১২৩৪৫৬৭৮৯০]+)[।.]\s+', '', t)
                cur_lines = []
                continue
            if started:
                cur_lines.append(t)
        flush_item()







        
        for p in paras:
            t = p.text.strip()
            if not t or re.search(r'Type\s*[:\-]\s*\w+', t, re.IGNORECASE):
                continue
            is_bold = p.runs and any(run.bold for run in p.runs if run.text.strip())
            is_num = re.match(r'^(\d+|[১২৩৪৫৬৭৮৯০]+)[।.]\s+.{5,}', t)
            if is_bold and is_num:
                flush_item()
                started = True
                cur_title = re.sub(r'^(\d+|[১২৩৪৫৬৭৮৯০]+)[।.]\s+', '', t)
                cur_lines = []
                continue
            if started:
                cur_lines.append(t)
        flush_item()

    return chunks

def search(query, kb, top_k=7):
    if not kb:
        return []
    qw = set(re.findall(r'\w+', query.lower()))
    scored = []
    for c in kb:
        w = set(re.findall(r'\w+', c.get("searchable", "").lower()))
        n = len(qw & w)
        if n > 0:
            scored.append((n, c))
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
    prompt = "You are a knowledge retrieval system. Answer the question using the provided references. Respond in the same language as the question. Always mention book name and item name/number.\n\nReferences:\n" + "\n\n".join(ctx) + "\n\nQuestion: " + query + "\nAnswer:"
    client = Groq(api_key=GROQ_API_KEY)
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=1024
    )
    return resp.choices[0].message.content

# UI
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
    st.subheader("📤 বই যোগ করুন")
    uf = st.file_uploader("DOCX ফাইল আপলোড করুন", type=["docx"])
    bn = st.text_input("বইয়ের নাম (ঐচ্ছিক)")
    if uf and st.button("যোগ করুন", type="primary"):
        name = bn or uf.name.replace(".docx", "")
        with st.spinner("প্রসেস হচ্ছে..."):
            nc = parse_docx(uf.read(), name)
            kd = load_kb()
            kd = [c for c in kd if c["book"] != name]
            kd.extend(nc)
            save_kb(kd)
            st.session_state.kb = kd
        st.success(str(len(nc)) + " টি আইটেম যোগ হয়েছে!")
        st.rerun()
    if books:
        st.divider()
        st.subheader("🗑️ বই মুছুন")
        db = st.selectbox("বই সিলেক্ট করুন", options=books)
        if st.button("মুছুন"):
            kd = load_kb()
            kd = [c for c in kd if c["book"] != db]
            save_kb(kd)
            st.session_state.kb = kd
            st.success("মুছে গেছে!")
            st.rerun()

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
else:
    if not kb:
        st.info("বাম দিক থেকে DOCX ফাইল আপলোড করুন।")
    else:
        st.info("উপরে প্রশ্ন লিখুন।")
