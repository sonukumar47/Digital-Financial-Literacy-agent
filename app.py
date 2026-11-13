"""
Digital Financial Literacy Agent — Streamlit UI
Powered by IBM Granite via watsonx.ai with RAG and multilingual support.
"""

import os
import streamlit as st
from dotenv import load_dotenv

from knowledge_base import get_all_documents
from rag_engine import build_vector_store, load_vector_store, build_rag_chain, ask_question
from translator import (
    SUPPORTED_LANGUAGES,
    detect_language,
    translate_to_english,
    translate_from_english,
    get_greeting,
)

load_dotenv()

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Digital Financial Literacy Agent",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* ---- Global ---- */
    body { font-family: 'Segoe UI', sans-serif; }
    .main { background-color: #000000; }

    /* ---- Header banner ---- */
    .header-banner {
        background: linear-gradient(135deg, #0f4c81 0%, #1a73e8 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .header-banner h1 { margin: 0; font-size: 2rem; }
    .header-banner p  { margin: 0.4rem 0 0; font-size: 1rem; opacity: 0.9; }

    /* ---- Chat bubbles ---- */
    .user-bubble {
        background: #1a73e8;
        color: white;
        padding: 0.75rem 1.1rem;
        border-radius: 18px 18px 4px 18px;
        margin: 0.5rem 0 0.5rem 20%;
        text-align: right;
        box-shadow: 0 2px 6px rgba(0,0,0,0.12);
    }
    .bot-bubble {
        background: #000000;
        color: #ffffff;
        padding: 0.75rem 1.1rem;
        border-radius: 18px 18px 18px 4px;
        margin: 0.5rem 20% 0.5rem 0;
        box-shadow: 0 2px 6px rgba(255,255,255,0.08);
        border-left: 4px solid #1a73e8;
    }
    .source-tag {
        font-size: 0.75rem;
        color: #a0aab4;
        margin-top: 0.4rem;
    }

    /* ---- Topic cards ---- */
    .topic-card {
        background: #000000;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
        cursor: pointer;
        transition: box-shadow 0.2s;
        color: #ffffff;
    }
    .topic-card:hover { box-shadow: 0 4px 12px rgba(255,255,255,0.15); }

    /* ---- Alert badges ---- */
    .badge-fraud   { background:#fee2e2; color:#dc2626; padding:2px 8px; border-radius:12px; font-size:0.78rem; }
    .badge-info    { background:#dbeafe; color:#1d4ed8; padding:2px 8px; border-radius:12px; font-size:0.78rem; }
    .badge-success { background:#dcfce7; color:#15803d; padding:2px 8px; border-radius:12px; font-size:0.78rem; }

    /* ---- Sidebar ---- */
    .sidebar-title { font-size:1.1rem; font-weight:700; color:#0f4c81; margin-bottom:0.5rem; }

    /* ---- Input area ---- */
    .stTextInput > div > div > input { border-radius: 24px; padding: 0.6rem 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------
def init_session():
    defaults = {
        "messages": [],           # list of {"role": "user"|"assistant", "content": str, "sources": list}
        "chain": None,
        "vector_store_ready": False,
        "selected_lang": "en",
        "auto_detect": True,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()


# ---------------------------------------------------------------------------
# RAG / Vector store bootstrap (cached)
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def get_rag_chain():
    """Build or load the FAISS index and return the RAG chain."""
    vs = load_vector_store()
    if vs is None:
        docs = get_all_documents()
        vs = build_vector_store(docs)
    return build_rag_chain(vs)


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-title">⚙️ Settings</div>', unsafe_allow_html=True)

    # Language selector
    lang_names = list(SUPPORTED_LANGUAGES.keys())
    selected_lang_name = st.selectbox(
        "🌐 Preferred Language",
        lang_names,
        index=0,
        help="Choose your language. Auto-detect is ON by default.",
    )
    st.session_state.selected_lang = SUPPORTED_LANGUAGES[selected_lang_name]

    auto_detect = st.toggle("Auto-detect language from input", value=True)
    st.session_state.auto_detect = auto_detect

    st.divider()

    # Quick-topic buttons
    st.markdown('<div class="sidebar-title">📚 Quick Topics</div>', unsafe_allow_html=True)

    topic_questions = {
        "💳 How to use UPI?":                    "How do I send money via UPI?",
        "🛡️ How to avoid online scams?":          "How can I protect myself from online financial scams?",
        "📈 What is a safe loan interest rate?":  "What is a safe interest rate for a personal loan?",
        "💰 How to create a budget?":             "How do I create a monthly budget?",
        "🏦 Best savings schemes in India?":      "What are the best savings instruments for beginners in India?",
        "📊 How to improve CIBIL score?":         "How can I improve my CIBIL credit score?",
        "🚨 Received suspicious UPI request?":   "I received a collect money request on UPI from an unknown number. What should I do?",
        "📱 Is my UPI app safe?":                 "What are the safety tips for using UPI apps?",
    }

    for label, question in topic_questions.items():
        if st.button(label, use_container_width=True, key=f"topic_{label}"):
            st.session_state["pending_question"] = question

    st.divider()

    # Clear chat
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown(
        """
        <small>
        <b>Powered by:</b><br>
        🔵 IBM Granite via watsonx.ai<br>
        📚 RAG with FAISS<br>
        🌍 Deep Translator<br><br>
        <b>Trusted Sources:</b><br>
        RBI • NPCI • SEBI • IRDAI<br>
        Ministry of Finance (GoI)
        </small>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="header-banner">
        <h1>💰 Digital Financial Literacy Agent</h1>
        <p>Your AI-powered guide to UPI, budgeting, safe banking & fraud prevention &nbsp;|&nbsp; Powered by <b>IBM Granite</b></p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Introductory cards (shown only when chat is empty)
# ---------------------------------------------------------------------------
if not st.session_state.messages:
    greeting = get_greeting(st.session_state.selected_lang)
    st.info(f"👋 {greeting}  \nAsk me anything about digital payments, loans, budgeting, or how to stay safe online!")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div class="topic-card">
                <b>📲 UPI Payments</b><br>
                <small>Send money, QR codes, safety tips & transaction limits</small>
            </div>
            """, unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="topic-card">
                <b>🛡️ Fraud Prevention</b><br>
                <small>Spot scams, protect your PIN, report cybercrime</small>
            </div>
            """, unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="topic-card">
                <b>📊 Interest Rates</b><br>
                <small>Home loans, personal loans, FD rates & EMI calculator guidance</small>
            </div>
            """, unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="topic-card">
                <b>💼 Personal Finance</b><br>
                <small>Net worth, insurance, credit score & investment basics</small>
            </div>
            """, unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            """
            <div class="topic-card">
                <b>🏦 Savings & Budgeting</b><br>
                <small>50-30-20 rule, PPF, FD, SIP and government schemes</small>
            </div>
            """, unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="topic-card">
                <b>🌐 Multilingual</b><br>
                <small>Ask in Hindi, Tamil, Telugu, Bengali & 8 more languages</small>
            </div>
            """, unsafe_allow_html=True,
        )

# ---------------------------------------------------------------------------
# Chat history display
# ---------------------------------------------------------------------------
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="user-bubble">🧑 {msg["content"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            sources_html = ""
            if msg.get("sources"):
                srcs = " &nbsp;•&nbsp; ".join(f"📖 {s}" for s in msg["sources"])
                sources_html = f'<div class="source-tag">Sources: {srcs}</div>'
            st.markdown(
                f'<div class="bot-bubble">🤖 {msg["content"]}{sources_html}</div>',
                unsafe_allow_html=True,
            )

# ---------------------------------------------------------------------------
# Chat input
# ---------------------------------------------------------------------------
with st.form(key="chat_form", clear_on_submit=True):
    cols = st.columns([8, 1])
    with cols[0]:
        user_input = st.text_input(
            label="Ask a financial question…",
            label_visibility="collapsed",
            placeholder="e.g. How do I send money via UPI?  |  UPI से पैसे कैसे भेजें?",
        )
    with cols[1]:
        submitted = st.form_submit_button("Send 🚀", use_container_width=True)

# Pick up sidebar topic-button clicks
if "pending_question" in st.session_state:
    pending = st.session_state.pop("pending_question")
    if pending:
        user_input = pending
        submitted = True

# ---------------------------------------------------------------------------
# Process query
# ---------------------------------------------------------------------------
if submitted and user_input.strip():
    raw_question = user_input.strip()

    # Language detection / override
    if st.session_state.auto_detect:
        detected_lang = detect_language(raw_question)
        response_lang = detected_lang
    else:
        response_lang = st.session_state.selected_lang

    # Translate to English for the RAG pipeline
    english_question = translate_to_english(raw_question, response_lang)

    # Store user message
    st.session_state.messages.append({"role": "user", "content": raw_question})

    # Load RAG chain (cached)
    with st.spinner("🔍 Retrieving relevant knowledge…"):
        try:
            chain = get_rag_chain()
        except Exception as e:
            st.error(
                f"⚠️ Could not connect to IBM watsonx.ai. "
                f"Please verify your API key and Project ID in the `.env` file.\n\n`{e}`"
            )
            st.stop()

    # Get answer
    with st.spinner("🤖 IBM Granite is thinking…"):
        try:
            result = ask_question(chain, english_question)
            english_answer = result["answer"]
            sources = result["sources"]
        except Exception as e:
            english_answer = (
                "I'm sorry, I encountered an error processing your question. "
                "Please try again or rephrase your question."
            )
            sources = []
            st.warning(f"LLM error: {e}")

    # Translate answer back to user's language
    if response_lang != "en":
        with st.spinner(f"🌐 Translating to {selected_lang_name}…"):
            final_answer = translate_from_english(english_answer, response_lang)
    else:
        final_answer = english_answer

    # Fraud/risk detection badge (keyword-based, quick UX hint)
    lower_answer = english_answer.lower()
    if any(w in lower_answer for w in ["scam", "fraud", "beware", "never share", "do not"]):
        final_answer = "⚠️ **Safety Alert:** " + final_answer
    elif any(w in lower_answer for w in ["government scheme", "free", "subsidy", "pmjdy"]):
        final_answer = "✅ **Government Scheme Info:** " + final_answer

    # Store assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": final_answer,
        "sources": sources,
    })

    st.rerun()


# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown(
    """
    <hr style="border:none;border-top:1px solid #444;margin-top:2rem;">
    <div style="text-align:center;color:#a0aab4;font-size:0.8rem;padding-bottom:1rem;">
        Digital Financial Literacy Agent &nbsp;|&nbsp; 
        Powered by <b>IBM Granite</b> &amp; <b>watsonx.ai</b> &nbsp;|&nbsp;
        Sources: RBI, NPCI, SEBI, IRDAI, Government of India &nbsp;|&nbsp;
        🚨 Cybercrime Helpline: <b>1930</b>
    </div>
    """,
    unsafe_allow_html=True,
)
