import os
import streamlit as st
from api_client import api_client

# Page Config
st.set_page_config(
    page_title="RAG Document Assistant",
    page_icon="📚",
    layout="wide"
)

# Modern Custom CSS Styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .answer-card {
        background-color: #1E293B;
        color: #F1F5F9;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 1.5rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        font-size: 1.05rem;
        line-height: 1.6;
    }
    .answer-card p {
        color: #F1F5F9 !important;
        margin-bottom: 0.5rem;
    }

    .source-badge {
        display: inline-block;
        background-color: #EFF6FF;
        color: #1D4ED8;
        border: 1px solid #BFDBFE;
        border-radius: 6px;
        padding: 0.35rem 0.75rem;
        font-size: 0.88rem;
        font-weight: 500;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown('<div class="main-header">📚 RAG-Powered Document Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Ask grounded questions about your Computer Science course notes and reference documents.</div>', unsafe_allow_html=True)

# Sidebar with System Status & Settings
with st.sidebar:
    st.header("⚙️ System Status")
    
    st.info(f"**Backend URL:**\n`{api_client.base_url}`")
    
    health_ok, health_data = api_client.check_health()
    if health_ok:
        st.success("🟢 Backend Connected")
        st.metric("Indexed Chunks", health_data.get("total_documents_indexed", 0))
        st.write(f"**Embedding Model:** `{health_data.get('embedding_model', 'N/A')}`")
        if health_data.get("ollama_connected"):
            st.success("🟢 Local Ollama LLM Ready")
        else:
            st.warning("🟡 Ollama Offline (Fallback Summary Mode)")
    else:
        st.error("🔴 Backend Disconnected")
        st.error(health_data.get("error", "Unable to connect to backend."))

    st.divider()
    st.markdown("### 📌 Instructions")
    st.markdown("""
    1. Enter your question about Operating Systems, Databases, Networks, or Software Engineering.
    2. Click **Submit Question**.
    3. View the grounded answer and exact document citations below.
    """)

# Main Chat / Query Interface
question_input = st.text_area(
    "Ask a question about your documents:",
    placeholder="e.g., What is virtual memory and why is paging used in operating systems?",
    height=100
)

col1, col2 = st.columns([1, 5])
with col1:
    submit_btn = st.button("🚀 Ask Question", use_container_width=True, type="primary")

if submit_btn:
    if not question_input.strip():
        st.warning("⚠️ Please enter a question before submitting.")
    else:
        with st.spinner("🔍 Searching document vector store and generating grounded answer..."):
            success, response = api_client.send_query(question_input.strip())
        
        if success:
            st.markdown("### 💡 Grounded Answer")
            answer_text = response.get("answer", "No answer returned.")
            st.markdown(f'<div class="answer-card">{answer_text}</div>', unsafe_allow_html=True)

            sources = response.get("sources", [])
            st.markdown("### 📄 Cited Sources")
            if sources:
                for idx, src in enumerate(sources, 1):
                    doc_name = src.get("document", "Unknown")
                    page_num = src.get("page", 1)
                    snippet = src.get("snippet")
                    
                    with st.expander(f"📌 Citation [{idx}]: {doc_name} — Page {page_num}"):
                        st.markdown(f"**Document:** `{doc_name}`")
                        st.markdown(f"**Page:** `{page_num}`")
                        if snippet:
                            st.markdown(f"**Context Excerpt:**\n_{snippet}_")
            else:
                st.info("No specific source citations were returned for this answer.")
        else:
            st.error(f"❌ Error: {response.get('error', 'Failed to retrieve answer from backend.')}")

# Quick Sample Questions Footer
st.divider()
st.markdown("#### 💡 Example Questions You Can Try:")
example_cols = st.columns(3)
with example_cols[0]:
    st.caption("• What is virtual memory?")
    st.caption("• Explain process vs thread.")
with example_cols[1]:
    st.caption("• What are ACID properties in DBMS?")
    st.caption("• Describe B-Tree indexing.")
with example_cols[2]:
    st.caption("• How does TCP 3-way handshake work?")
    st.caption("• Explain REST architectural constraints.")
