# Autonomous Research Analyst

A full-stack, recruiter-ready AI Research Analyst built with Python 3.10+, Streamlit, and Google Gemini. This application allows you to ingest documents, research through a knowledge base using RAG, and generate structured reports and presentations with citations.

## 🚀 Key Features
- **Intelligent Ingestion**: Support for PDF, DOCX, and Web URLs.
- **RAG Engine**: Powered by ChromaDB and Sentence Transformers for accurate context retrieval.
- **Gemini Integration**: High-fidelity insights and summaries using Gemini 1.5 Flash.
- **Professional Exports**: Export findings to Markdown, PDF, or PowerPoint slides.
- **Premium UI**: Clean, responsive dashboard with glassmorphism and real-time feedback.
- **Citation Tracking**: Trace every insight back to its original source.

## 🛠️ Setup Instructions

### 1. Environment Setup
Create and activate the virtual environment:
```powershell
# Windows
python -m venv analyst_env
.\analyst_env\Scripts\activate

# Linux/Mac
python3.10 -m venv analyst_env
source analyst_env/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configuration
- Create a `.env` file in the root directory.
- Add your Google Gemini API Key:
  ```env
  GOOGLE_API_KEY=your_gemini_api_key_here
  ```

### 4. Run the Application
```bash
streamlit run app.py
```

## 📝 Usage Guide
1. **Login**: Use the default password `analyst123` (or set custom in `auth.py`).
2. **Setup**: Enter your Gemini API key in the sidebar and click "Initialize Engine".
3. **Ingest**: Go to the **Knowledge Base** tab to upload documents or add URLs.
4. **Research**: Ask questions in the **Research** tab. View citations in the right-hand panel.
5. **Report**: Create reports and export them as PDF/Markdown/Slides in the **Reports** tab.

## 🛡️ Error Handling
The application features robust defensive coding:
- **Empty State Checks**: Prompts user for keys and initialization.
- **Fail-safe Ingestion**: Handles corrupt files and network errors gracefully with UI alerts.
- **Async Processing**: Integrated session states to prevent UI lockup.
- **Fallback Logic**: Provides clear messages when information is missing from the database.

---
*Built for the Google DeepMind & Kaggle Hackathon.*
