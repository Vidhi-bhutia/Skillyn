import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from helper import extract_pdf_text, prepare_prompt, get_gemini_response
from unittest.mock import patch, MagicMock
import io

# --- Test extract_pdf_text ---
def test_extract_pdf_text_valid_pdf():
    # Create a simple PDF in memory
    from PyPDF2 import PdfWriter
    pdf_bytes = io.BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    writer.write(pdf_bytes)
    pdf_bytes.seek(0)
    # Should not raise error, but will return empty string (no text)
    with pytest.raises(Exception):
        extract_pdf_text(pdf_bytes)

def test_extract_pdf_text_empty_file():
    empty_pdf = io.BytesIO(b"")
    with pytest.raises(Exception):
        extract_pdf_text(empty_pdf)

# --- Test prepare_prompt ---
def test_prepare_prompt_valid():
    text = "Sample resume text"
    jd = "Sample job description"
    prompt = prepare_prompt(text, jd)
    assert "Sample resume text" in prompt
    assert "Sample job description" in prompt
    assert "Application Tracking System" in prompt

def test_prepare_prompt_empty_text():
    with pytest.raises(ValueError):
        prepare_prompt("", "JD")
    with pytest.raises(ValueError):
        prepare_prompt("Resume", "")

# --- Test get_gemini_response ---
@patch("helper.genai.GenerativeModel")
def test_get_gemini_response_valid_json(mock_model):
    mock_instance = MagicMock()
    mock_instance.generate_content.return_value.text = '{"JD Match": "90", "Missing Keywords": ["Python"], "Profile Summary": "Good"}'
    mock_model.return_value = mock_instance
    prompt = "test prompt"
    result = get_gemini_response(prompt)
    assert 'JD Match' in result
    assert 'Missing Keywords' in result
    assert 'Profile Summary' in result

@patch("helper.genai.GenerativeModel")
def test_get_gemini_response_invalid_json(mock_model):
    mock_instance = MagicMock()
    mock_instance.generate_content.return_value.text = 'Not a JSON response'
    mock_model.return_value = mock_instance
    prompt = "test prompt"
    with pytest.raises(Exception):
        get_gemini_response(prompt)

@patch("helper.genai.GenerativeModel")
def test_get_gemini_response_partial_json(mock_model):
    mock_instance = MagicMock()
    mock_instance.generate_content.return_value.text = 'Some text {"JD Match": "80", "Missing Keywords": [], "Profile Summary": "Ok"} more text'
    mock_model.return_value = mock_instance
    prompt = "test prompt"
    result = get_gemini_response(prompt)
    assert 'JD Match' in result
    assert 'Missing Keywords' in result
    assert 'Profile Summary' in result
