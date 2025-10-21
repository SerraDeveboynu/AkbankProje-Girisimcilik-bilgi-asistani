import os
import streamlit as st
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import numpy as np
import chromadb
from chromadb.config import Settings
from pathlib import Path

# ========== SAYFA ==========
st.set_page_config(page_title="Girişimcilik Bilgi Asistanı", layout="wide")
st.title("💬 Girişimcilik Bilgi Asistanı")
st.caption("TÜBİTAK, KOSGEB ve TEKNOFEST metinlerinden RAG ile yanıt üretir. (Gemini 2.5-flash)")

# ========== API ANAHTARI ==========
API_KEY = st.secrets.get("GENAI_API_KEY", None) or os.getenv("GENAI_API_KEY")
if not API_KEY:
    st.error(" API anahtarı bulunamadı. Lütfen Streamlit Secrets veya ortam değişkenine 'GENAI_API_KEY' ekleyin.")
    st.stop()

genai.configure(api_key=API_KEY)
gmodel = genai.GenerativeModel("gemini-2.5-flash")

# ========== YOLLAR ==========
DATA_DIR = Path("./data")
DB_DIR = Path("./girisim_db")
DB_DIR.mkdir(exist_ok=True)

# ========== EMBEDDING ==========
@st.cache_resource
def load_embedder():
    return SentenceTransformer("intfloat/multilingual-e5-small")

embedder = load_embedder()

def embed_texts(texts):
    vecs = embedder.encode(texts, normalize_embeddings=True)
    return np.asarray(vecs, dtype=np.float32)

def split_text(text, chunk_size=800, overlap=120):
    chunks, start, n = [], 0, len(text)
    while start < n:
        end = min(start + chunk_size, n)
        chunks.append(text[start:end])
        if end == n:
            break
        start = end - overlap
    return chunks

# ========== CHROMADB ==========
client = chromadb.PersistentClient(path=str(DB_DIR), settings=Settings(allow_reset=True))
collection = client.get_or_create_collection(name="girisim", metadata={"hnsw:space": "cosine"})

def rebuild_index_from_data_dir():
    if not DATA_DIR.exists():
        raise RuntimeError("data/ klasörü bulunamadı.")
    texts, metadatas, ids = [], [], []
    for f in DATA_DIR.glob("*.txt"):
        raw = f.read_text(encoding="utf-8", errors="ignore")
        parts = split_text(raw, 800, 120)
        for i, p in enumerate(parts):
            texts.append(p)
            metadatas.append({"source": f.name, "part": i+1})
            ids.append(f"{f.stem}-{i+1:05d}")
    if not texts:
        raise RuntimeError("data/ klasöründe .txt dosyası yok.")
global collection
try:
    client.delete_collection(name="girisim")
except Exception:
    pass

collection = client.get_or_create_collection(
    name="girisim",
    metadata={"hnsw:space": "cosine"}
)

vecs = embed_texts(texts)
collection.add(ids=ids, documents=texts, embeddings=vecs.tolist(), metadatas=metadatas)
return len(texts)

def retrieve(query, k=4):
    qvec = embed_texts([query])[0].tolist()
    res = collection.query(query_embeddings=[qvec], n_results=k, include=["documents", "metadatas"])
    docs = res["documents"][0]
    metas = res["metadatas"][0]
    return list(zip(docs, metas))

SYSTEM_PROMPT = (
    "Sen Türkçe konuşan bir girişimcilik danışmanı asistansın. "
    "Cevaplarını verilen içerik parçalarına dayandır; emin değilsen 'bilmiyorum' de. "
    "Yanıtlarında [Kaynak] numaralarını parantez içinde belirt."
)

# ========== ARAYÜZ ==========
st.markdown("### 📂 Belgeler")
colA, colB, colC = st.columns([1, 1, 1])

with colA:
    if st.button("./data klasöründen indeksi oluştur (veya yenile)"):
        try:
            n = rebuild_index_from_data_dir()
            st.success(f" İndeks başarıyla oluşturuldu. Toplam parça: {n}")
        except Exception as e:
            st.error(f" Hata: {e}")

with colB:
    k = st.slider("🔍 Aranacak parça sayısı (k)", 1, 8, 4, 1)

st.markdown("---")
st.markdown("### 💬 Soru Sor")

if "chat" not in st.session_state:
    st.session_state.chat = []

for m in st.session_state.chat:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Örn: 'KOSGEB genç girişimcilere hangi destekleri sağlar?'"):
    st.session_state.chat.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Yanıt hazırlanıyor..."):
            try:
                retrieved = retrieve(prompt, k=k)
                if not retrieved:
                    raise RuntimeError("İndeks boş. Önce 'İndeksi oluştur' butonuna basın.")
                ctx = "\n\n".join([f"[Kaynak {i+1}] {doc}" for i, (doc, meta) in enumerate(retrieved)])
                full_prompt = (
                    f"{SYSTEM_PROMPT}\n\n"
                    f"Kullanıcı sorusu: {prompt}\n\n"
                    f"İlgili içerik parçaları:\n{ctx}\n\n"
                    "Yanıtında kullandığın [Kaynak] numaralarını parantez içinde belirt."
                )
                resp = gmodel.generate_content(full_prompt)
                answer = resp.text if hasattr(resp, "text") else str(resp)
                st.markdown(answer)

                with st.expander("📎 Kullanılan kaynak parçalar"):
                    for i, (doc, meta) in enumerate(retrieved, 1):
                        src = meta.get("source", "dosya")
                        part = meta.get("part", "?")
                        snippet = (doc[:300] + "…") if len(doc) > 300 else doc
                        st.markdown(f"**Kaynak {i}** — `{src}` (parça {part})\n\n> {snippet}\n\n---")

            except Exception as e:
                answer = f" Hata: {e}"
                st.error(answer)

    st.session_state.chat.append({"role": "assistant", "content": answer})


