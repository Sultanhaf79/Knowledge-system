import streamlit as st
import os, json, re, base64, requests
from docx import Document

st.set_page_config(page_title="Admin Panel", page_icon="🔧", layout="wide")

st.set_page_config(page_title="Admin Panel", page_icon="🔧", layout="wide")

st.markdown("""
<style>
.stDeployButton {display:none;}
#MainMenu {display:none;}
footer {display:none;}
header {display:none;}
[data-testid="stToolbar"] {display:none;}
[data-testid="stHeader"] {display:none;}
[data-testid="stDecoration"] {display:none;}
.viewerBadge_container__1QSob {display:none;}
.viewerBadge_link__1S137 {display:none;}
#stDecoration {display:none;}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
.stDeployButton {display:none;}
#MainMenu {display:none;}
footer {display:none;}
header {display:none;}
[data-testid="stToolbar"] {display:none;}
</style>
""", unsafe_allow_html=True)

GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", "")
GITHUB_REPO  = st.secrets.get("GITHUB_REPO", "")
KB_FILE      = "knowledge_base.json"
GH_API       = "https://api.github.com/repos/" + GITHUB_REPO + "/contents/" + KB_FILE

def load_kb():
    try:
        r = requests.get(GH_API, headers={"Authorization": "token " + GITHUB_TOKEN})
        if r.status_code == 200:
            content = base64.b64decode(r.json()["content"]).decode("utf-8")
            if content.strip():
                return json.loads(content)
    except:
        pass
    return []

def save_kb(data):
    try:
        content = base64.b64encode(json.dumps(data, ensure_ascii=False, indent=2).encode()).decode()
        headers = {"Authorization": "token " + GITHUB_TOKEN}
        sha = None
        r = requests.get(GH_API, headers=headers)
        if r.status_code == 200:
            sha = r.json().get("sha")
        payload = {"message": "update kb", "content": content}
        if sha:
            payload["sha"] = sha
        resp = requests.put(GH_API, headers=headers, json=payload)
        return resp.status_code in [200, 201]
    except Exception as e:
        st.error("Save error: " + str(e))
        return False

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
                    "book": book_name, "type": "CQ", "topic": cur_topic,
                    "cq_num": cur_cq, "text": full, "parts": dict(cur_parts),
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
                cur_cq = None; cur_lines = []; cur_parts = {}; cur_part = None
                continue
            cm = re.match(r'^([১২৩৪৫৬৭৮৯০1-9]\d*)[।.]', t)
            if cm:
                flush_cq()
                cur_cq = cm.group(1); cur_lines = [t]; cur_parts = {}; cur_part = None
                continue
            pm = re.match(r'^([কখগঘ])[।.]\s*(.*)', t)
            if pm:
                cur_part = pm.group(1)
                cur_parts[cur_part] = pm.group(2)
                if cur_lines: cur_lines.append(t)
                continue
            if cur_cq:
                if cur_part and cur_part in cur_parts:
                    cur_parts[cur_part] += " " + t
                cur_lines.append(t)
        flush_cq()

    elif content_type == "MCQ":
        cur_q = None; cur_lines = []; cur_opts = {}

        def flush_mcq():
            if cur_q and cur_lines:
                full = "\n".join(cur_lines)
                chunks.append({
                    "book": book_name, "type": "MCQ", "topic": "MCQ",
                    "cq_num": cur_q, "text": full, "parts": dict(cur_opts),
                    "searchable": book_name + " MCQ " + full + " " + " ".join(cur_opts.values())
                })

        for p in paras:
            t = p.text.strip()
            if not t or re.search(r'Type\s*[:\-]\s*\w+', t, re.IGNORECASE): continue
            qm = re.match(r'^([১২৩৪৫৬৭৮৯০1-9]\d*)[।.]', t)
            if qm:
                flush_mcq()
                cur_q = qm.group(1); cur_lines = [t]; cur_opts = {}
                continue
            om = re.match(r'^[\(\[]?([কখগঘABCDabcd])[)\]।.]\s*(.*)', t)
            if om and cur_q:
                cur_opts[om.group(1)] = om.group(2); cur_lines.append(t); continue
            am = re.search(r'উত্তর\s*[:\-।]?\s*(.*)', t)
            if am and cur_q:
                cur_opts["Ans"] = am.group(1); cur_lines.append(t); continue
            if cur_q: cur_lines.append(t)
        flush_mcq()

    else:
        cur_title = None; cur_lines = []; started = False

        def flush_item():
            if cur_lines and cur_title:
                full = "\n".join(cur_lines)
                chunks.append({
                    "book": book_name, "type": content_type, "topic": content_type,
                    "cq_num": cur_title, "text": full, "parts": {},
                    "searchable": book_name + " " + content_type + " " + cur_title + " " + cur_title + " " + cur_title + " " + full
                })

        for p in paras:
            t = p.text.strip()
            if not t or re.search(r'Type\s*[:\-]\s*\w+', t, re.IGNORECASE): continue
            is_bold = p.runs and any(run.bold for run in p.runs if run.text.strip())
            is_num = re.match(r'^(\d+|[১২৩৪৫৬৭৮৯০]+)[।.]\s*.{3,}', t)
            if is_bold and (is_num or len(t) < 100):
                flush_item()
                started = True
                cur_title = re.sub(r'^(\d+|[১২৩৪৫৬৭৮৯০]+)[।.]\s*\*+\s*', '', t).strip('* ').strip()

                
                cur_lines = []
                continue
            if started:
                cur_lines.append(t)
        flush_item()

    return chunks

# UI
st.title("Admin Panel")
st.caption("AI Knowledge Base - Add & Remove Books")

kb = load_kb()
books = sorted(set(c["book"] for c in kb)) if kb else []

col1, col2 = st.columns(2)
col1.metric("Total Books", len(books))
col2.metric("Total Items", len(kb))

st.divider()
st.subheader("Add Book")
uf = st.file_uploader("Upload DOCX file", type=["docx"])
bn = st.text_input("Book name (optional)")

if uf and st.button("Add", type="primary"):
    name = bn or uf.name.replace(".docx", "")
    with st.spinner("Processing..."):
        nc = parse_docx(uf.read(), name)
        kd = load_kb()
        kd = [c for c in kd if c["book"] != name]
        kd.extend(nc)
        saved = save_kb(kd)
    if saved:
        st.success(str(len(nc)) + " items added successfully!")
    else:
        st.error("Save failed!")

st.divider()

if books:
    st.subheader("Delete Book")
    db = st.selectbox("Select book", options=books)
    if st.button("Delete", type="secondary"):
        kd = load_kb()
        kd = [c for c in kd if c["book"] != db]
        saved = save_kb(kd)
        if saved:
            st.success("Deleted!")
        else:
            st.error("Delete failed!")

    st.divider()
    st.subheader("Book List")
    for b in books:
        cnt = sum(1 for c in kb if c["book"] == b)
        st.write("- " + b + " (" + str(cnt) + " items)")
