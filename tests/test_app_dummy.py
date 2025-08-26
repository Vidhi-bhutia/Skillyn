import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from unittest.mock import patch, MagicMock
import app

# These are basic smoke/integration tests for the Streamlit app logic.
# UI testing is limited in pure pytest; for full UI tests, use streamlit-testing tools or playwright.

def test_main_runs(monkeypatch):
    # Patch Streamlit methods to avoid actual UI rendering
    monkeypatch.setattr(app, "st", MagicMock())
    monkeypatch.setattr(app, "load_dotenv", lambda: None)
    monkeypatch.setattr(app, "configure_genai", lambda x: None)
    monkeypatch.setattr(app, "extract_pdf_text", lambda x: "resume text")
    monkeypatch.setattr(app, "prepare_prompt", lambda x, y: "prompt")
    monkeypatch.setattr(app, "get_gemini_response", lambda x: '{"JD Match": "80", "Missing Keywords": [], "Profile Summary": "Good"}')
    # Should not raise error
    app.main()

# For more advanced Streamlit UI tests, use streamlit-testing or playwright.
