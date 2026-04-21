import streamlit as st
import os
from research_engine import ResearchEngine
from exporter import ReportExporter
from auth import check_password
from dotenv import load_dotenv
import base64

load_dotenv()

# Page Config
st.set_page_config(
    page_title="NEURAL Research Analyst v2",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Advanced Neural Theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    :root {
        --primary: #00f2fe;
        --secondary: #4facfe;
        --bg-dark: #0a0c10;
        --glass: rgba(255, 255, 255, 0.03);
        --border: rgba(255, 255, 255, 0.1);
    }

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at 50% 0%, #16213e 0%, #0a0c10 100%);
    }

    /* Glassmorphism Containers */
    .neural-card {
        background: var(--glass);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid var(--border);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    
    .neural-card:hover {
        border: 1px solid rgba(0, 242, 254, 0.3);
    }

    /* Gradient Text */
    .gradient-text {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid var(--border);
    }

    /* Custom Input */
    .stTextInput>div>div>input {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid var(--border) !important;
        color: white !important;
        border-radius: 12px !important;
    }

    /* Button Styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        color: #0c0e12;
        border: none;
        border-radius: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 12px 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.5);
        color: #0c0e12;
    }

    /* Metric Styling */
    [data-testid="stMetricValue"] {
        color: var(--primary);
        font-size: 2.5rem;
    }

    /* Hide Streamlit elements for cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Authentication
if not check_password():
    st.stop()

# Initialize Session States
if "engine" not in st.session_state:
    st.session_state.engine = None
if "ppt_ready" not in st.session_state:
    st.session_state.ppt_ready = False
if "ppt_path" not in st.session_state:
    st.session_state.ppt_path = ""

# Sidebar
with st.sidebar:
    st.markdown("<h2 class='gradient-text'>NEURAL V2</h2>", unsafe_allow_html=True)
    st.caption("Advanced Autonomous Research Agent")
    st.divider()
    
    api_key = st.text_input("Gemini API Key", type="password", value=os.getenv("GOOGLE_API_KEY", ""))
    
    if st.button("Initialize Systems"):
        if api_key:
            try:
                with st.spinner("Calibrating Neural Pathways..."):
                    st.session_state.engine = ResearchEngine(api_key=api_key)
                st.success("Core Online")
            except Exception as e:
                st.error(f"Sync Failed: {e}")
        else:
            st.warning("Credential Required")
            
    st.divider()
    
    if st.session_state.engine:
        stats = st.session_state.engine.get_stats()
        st.metric("Neural Memory Chunks", stats["document_chunks"])
        
        if st.button("Purge Database", type="secondary"):
            st.session_state.engine.clear_database()
            st.rerun()

# Main Header
st.markdown("<h1 class='gradient-text'>Autonomous Research Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

if not st.session_state.engine:
    st.warning("📡 Please initialize the engine from the sidebar to establish connection.")
    st.stop()

# Dashboard Layout
tab_lab, tab_ingest, tab_output = st.tabs(["🧬 Research Lab", "📥 Data Ingestion", "📈 Final Reports"])

# --- Research Lab ---
with tab_lab:
    col_input, col_viz = st.columns([2, 1])
    
    with col_input:
        st.markdown("<div class='neural-card'>", unsafe_allow_html=True)
        st.markdown("### 🧠 Intelligence Interface")
        query = st.chat_input("What would you like me to analyze today?")
        
        if query:
            try:
                # User Message
                with st.chat_message("user"):
                    st.write(query)
                
                # Assistant Processing
                with st.chat_message("assistant"):
                    with st.status("Searching Knowledge Base...", expanded=True) as status:
                        result = st.session_state.engine.query(query)
                        status.update(label="Analysis Complete", state="complete", expanded=False)
                        st.write(result["answer"])
                        st.session_state.last_result = result
            except Exception as e:
                st.error(f"Neural Error: {str(e)}")
        elif "last_result" in st.session_state:
             with st.chat_message("assistant"):
                st.write(st.session_state.last_result["answer"])
        
        st.markdown("</div>", unsafe_allow_html=True)

    with col_viz:
        st.markdown("<div class='neural-card'>", unsafe_allow_html=True)
        st.markdown("### 🔍 Citations & Sources")
        if "last_result" in st.session_state:
            res = st.session_state.last_result
            for i, (source, snippet) in enumerate(zip(res["sources"], res["snippets"])):
                with st.expander(f"📌 {source[:30]}"):
                    st.caption(f"Source ID: {i+1}")
                    st.markdown(f"*{snippet}*")
        else:
            st.info("No active analysis")
        st.markdown("</div>", unsafe_allow_html=True)

# --- Ingestion ---
with tab_ingest:
    st.markdown("<div class='neural-card'>", unsafe_allow_html=True)
    st.markdown("### 🔋 Powering the Brain")
    
    up, url = st.columns(2)
    
    with up:
        st.markdown("#### Cloud Upload")
        uploaded_files = st.file_uploader("Select PDF/DOCX Data", accept_multiple_files=True)
        if st.button("Process Documents"):
            if uploaded_files:
                for f in uploaded_files:
                    path = os.path.join("./data", f.name)
                    os.makedirs("./data", exist_ok=True)
                    with open(path, "wb") as bf: bf.write(f.getbuffer())
                    with st.spinner(f"Ingesting {f.name}..."):
                        st.session_state.engine.ingest_file(path, f.name)
                    os.remove(path)
                st.success("New knowledge integrated.")
                st.rerun()
    
    with url:
        st.markdown("#### Neural Web Scraping")
        target_link = st.text_input("Source URL")
        if st.button("Fetch URL"):
            if target_link:
                with st.spinner("Scraping and Vectorizing..."):
                    st.session_state.engine.ingest_url(target_link)
                st.success("Web knowledge synchronized.")
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- Output & Export ---
with tab_output:
    if "last_result" in st.session_state:
        st.markdown("<div class='neural-card'>", unsafe_allow_html=True)
        st.markdown("### 📝 Report Preparation")
        
        topic = st.text_input("Report Title", value="Intelligence Briefing")
        content = st.text_area("Findings", value=st.session_state.last_result["answer"], height=400)
        
        st.divider()
        b1, b2, b3 = st.columns(3)
        
        with b1:
             if st.button("💾 Generate Markdown"):
                path = ReportExporter.to_markdown(content)
                with open(path, "rb") as f:
                    st.download_button("Download MD", f, file_name=path)
                    
        with b2:
            if st.button("📝 Generate PDF"):
                path = ReportExporter.to_pdf(content)
                with open(path, "rb") as f:
                    st.download_button("Download PDF", f, file_name=path)
        
        with b3:
            # Fix PPT Logic
            if st.button("📊 Prepare Slides"):
                # Format content with markers if missing to help the exporter
                formatted_content = content
                if "## " not in content:
                    formatted_content = "## Summary\n" + content
                
                st.session_state.ppt_path = ReportExporter.to_slides(topic, formatted_content)
                st.session_state.ppt_ready = True
                st.success("Presentation Ready")

            if st.session_state.ppt_ready:
                with open(st.session_state.ppt_path, "rb") as f:
                    st.download_button(
                        label="🚀 Download Presentation (PPTX)",
                        data=f,
                        file_name=st.session_state.ppt_path,
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                    )
        
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("📊 Synthesize research to generate final reports.")

# Final Footer
st.markdown("<div style='text-align: center; color: rgba(255,255,255,0.2); margin-top: 50px;'>Neural Analyst Engine v2.5 | 2026 Edition</div>", unsafe_allow_html=True)
