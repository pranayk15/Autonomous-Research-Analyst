import streamlit as st
import os
from research_engine import ResearchEngine
from exporter import ReportExporter
from auth import check_password
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

# Page Config
st.set_page_config(
    page_title="Autonomous Research Analyst",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background-color: #0f1116;
        color: #ffffff;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #6e8efb 0%, #a777e3 100%);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(110, 142, 251, 0.4);
    }
    
    .stTextInput>div>div>input {
        background-color: #1a1e26;
        color: white;
        border: 1px solid #2d343f;
        border-radius: 8px;
    }
    
    .card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    
    .sidebar .sidebar-content {
        background-color: #1a1e26;
    }
    
    h1, h2, h3 {
        color: #6e8efb;
    }

    /* Citation Box */
    .citation-box {
        background: rgba(110, 142, 251, 0.1);
        border-left: 4px solid #6e8efb;
        padding: 10px;
        margin: 10px 0;
        font-size: 0.9em;
    }
</style>
""", unsafe_allow_html=True)

# Authentication
if not check_password():
    st.stop()

# Initialize Engine
if "engine" not in st.session_state:
    st.session_state.engine = None

# Sidebar Configuration
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=100)
    st.title("Settings")
    
    api_key = st.text_input("Gemini API Key", type="password", value=os.getenv("GOOGLE_API_KEY", ""))
    
    if st.button("Initialize Engine"):
        if api_key:
            try:
                with st.spinner("Setting up Research Brain..."):
                    st.session_state.engine = ResearchEngine(api_key=api_key)
                st.success("Engine Ready!")
            except Exception as e:
                st.error(f"Initialization Failed: {e}")
        else:
            st.warning("Please enter a valid API Key.")
            
    st.divider()
    
    if st.session_state.engine:
        stats = st.session_state.engine.get_stats()
        st.metric("Total Knowledge Chunks", stats["document_chunks"])
        
        if st.button("Clear Database", type="secondary"):
            st.session_state.engine.clear_database()
            st.rerun()

# Main UI
st.title("🧬 Autonomous Research Analyst")
st.markdown("Automated insights from your documents and the web.")

if not st.session_state.engine:
    st.info("👈 Please initialize the Research Engine in the sidebar to get started.")
    st.stop()

tab_research, tab_knowledge, tab_export = st.tabs(["🔍 Research", "📚 Knowledge Base", "📝 Reports & Export"])

# --- Research Tab ---
with tab_research:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Ask your Assistant")
        query = st.text_input("Enter your research query...", placeholder="e.g. What are the key trends in the Q3 market data?")
        
        if st.button("Run Analysis"):
            if query:
                try:
                    with st.spinner("Analyzing data and generating insights..."):
                        # Run query
                        result = st.session_state.engine.query(query)
                        
                        st.session_state.last_result = result
                        st.markdown("#### Analysis Findings")
                        st.write(result["answer"])
                        
                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")
            else:
                st.warning("Please enter a query.")
        
        if "last_result" in st.session_state:
            st.divider()
            st.markdown("### Usage Tracking")
            st.caption(f"Queries this session: {st.session_state.get('query_count', 0)}")

    with col2:
        st.markdown("### Citations & Sources")
        if "last_result" in st.session_state:
            res = st.session_state.last_result
            for i, (source, snippet) in enumerate(zip(res["sources"], res["snippets"])):
                with st.expander(f"Source {i+1}: {source[:30]}..."):
                    st.markdown(f"<div class='citation-box'>{snippet}</div>", unsafe_allow_html=True)
                    st.caption(f"Full source: {source}")
        else:
            st.info("Run an analysis to see sources.")

# --- Knowledge Base Tab ---
with tab_knowledge:
    st.markdown("### Ingest Knowledge")
    
    upload_col, url_col = st.columns(2)
    
    with upload_col:
        st.markdown("#### Upload Documents")
        uploaded_files = st.file_uploader("Upload PDF, DOCX, or TXT", accept_multiple_files=True)
        
        if st.button("Process Uploads"):
            if uploaded_files:
                for uploaded_file in uploaded_files:
                    try:
                        # Save temp file
                        temp_path = os.path.join("./data", uploaded_file.name)
                        os.makedirs("./data", exist_ok=True)
                        with open(temp_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        with st.spinner(f"Ingesting {uploaded_file.name}..."):
                            msg = st.session_state.engine.ingest_file(temp_path, uploaded_file.name)
                        st.success(msg)
                        
                        # Cleanup temp file
                        os.remove(temp_path)
                    except Exception as e:
                        st.error(f"Failed to ingest {uploaded_file.name}: {e}")
            else:
                st.warning("No files uploaded.")

    with url_col:
        st.markdown("#### Ingest Web URL")
        url = st.text_input("Enter URL (e.g. Wiki or News article)")
        if st.button("Ingest URL"):
            if url:
                try:
                    with st.spinner(f"Scraping {url}..."):
                        msg = st.session_state.engine.ingest_url(url)
                    st.success(msg)
                except Exception as e:
                    st.error(f"Failed to ingest URL: {e}")

# --- Export Tab ---
with tab_export:
    st.markdown("### Generate & Export Report")
    
    if "last_result" in st.session_state:
        report_topic = st.text_input("Report Topic", value="Market Research Findings")
        report_content = st.text_area("Report Content (Markdown)", value=st.session_state.last_result["answer"], height=300)
        
        col_md, col_pdf = st.columns(2)
        
        with col_md:
            if st.button("Export Markdown"):
                path = ReportExporter.to_markdown(report_content)
                with open(path, "rb") as f:
                    st.download_button("Download MD", f, file_name=path)
        
        with col_pdf:
            if st.button("Export PDF"):
                path = ReportExporter.to_pdf(report_content)
                with open(path, "rb") as f:
                    st.download_button("Download PDF", f, file_name=path)
    else:
        st.info("Run an analysis first to generate a report.")

# Footer
st.divider()
st.caption("AI Research Analyst | Built with Streamlit & Google Gemini")
