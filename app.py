import streamlit as st
import fitz  # PyMuPDF
from transformers import pipeline
from utils import clean_text, chunk_text
from model import load_model
# -------------------------------
# Load Model (runs once)
# -------------------------------

st.set_page_config(page_title="Research Summarizer", layout="wide")
@st.cache_resource
def load_model():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_model()

# -------------------------------
# Functions
# -------------------------------

def extract_text(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def clean_text(text):
    text = text.replace('\n', ' ')
    text = text.replace('  ', ' ')
    return text

def chunk_text(text, max_chunk=500):
    words = text.split()
    return [" ".join(words[i:i+max_chunk]) for i in range(0, len(words), max_chunk)]

def extract_insights(text):
    insights = []
    sentences = text.split('.')
    
    for s in sentences:
        if "we propose" in s.lower() or "we present" in s.lower():
            insights.append(s.strip())
    
    return insights

# -------------------------------
# UI
# -------------------------------



st.title("📄 Research Paper Summarizer")
st.write("Upload a research paper and get instant summary + insights")

uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

if uploaded_file:
    st.info("⏳ Processing... please wait")

    text = extract_text(uploaded_file)
    cleaned_text = clean_text(text)
    chunks = chunk_text(cleaned_text)

    summaries = []
    for chunk in chunks[:5]:
        summary = summarizer(chunk, max_length=150, min_length=50, do_sample=False)
        summaries.append(summary[0]['summary_text'])

    final_summary = " ".join(summaries)

    st.subheader("🧠 Summary")
    st.write(final_summary)

    insights = extract_insights(cleaned_text)

    st.subheader("⭐ Key Insights")
    for i in insights[:5]:
        st.write("- " + i)

import streamlit as st
from utils import clean_text, chunk_text
from model import load_model

st.title("📄 AI Research Paper Summarizer")

model_choice = st.selectbox("Choose Model", ["BART", "T5"])

model = load_model(model_choice)