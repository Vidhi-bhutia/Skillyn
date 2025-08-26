# Skillyn - Smart ATS Resume Analyzer

Skillyn is an intelligent, user-friendly web application that leverages Google Gemini AI to analyze resumes against job descriptions. It provides actionable feedback, highlights missing keywords, and suggests improvements to help candidates optimize their resumes for Applicant Tracking Systems (ATS).

## Features

- **Resume & Job Description Analysis:**
	- Upload your resume (PDF) and paste a job description to receive a detailed match analysis.
- **ATS Match Percentage:**
	- Instantly see how well your resume matches the job description as a percentage.
- **Missing Keywords:**
	- Identify important keywords from the job description that are missing in your resume.
- **Profile Summary & Feedback:**
	- Get a concise summary of your profile and personalized, actionable feedback for improvement.
- **Modern UI:**
	- Clean, responsive interface with custom styling for an enhanced user experience.

## How It Works

1. **User uploads a resume (PDF) and pastes a job description.**
2. **The app extracts text from the PDF and prepares a prompt for the Gemini AI model.**
3. **Gemini AI analyzes the resume against the job description and returns a structured JSON response.**
4. **The app displays:**
	 - ATS match percentage
	 - List of missing keywords
	 - Profile summary and improvement feedback

## Live Demo

You can try Skillyn instantly, no installation required:

👉 **[Skillyn](https://skillyn.streamlit.app/)**

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Vidhi-bhutia/Skillyn.git
cd Skillyn
```

### 2. Create and Activate a Virtual Environment (Recommended)
```bash
python -m venv skillyn
# On Windows:
skillyn\Scripts\activate
# On macOS/Linux:
source skillyn/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Google Gemini API Key
- Obtain your Google Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
- Create a `.env` file in the project root and add:
	```env
	GOOGLE_API_KEY=your_api_key_here
	```

### 5. Run the Application
```bash
streamlit run app.py
```
- The app will open in your browser at `http://localhost:8501` by default.

## Usage

1. **Paste the job description** in the provided text area.
2. **Upload your resume** as a PDF file.
3. Click **Analyze**.
4. View your ATS match score, missing keywords, and personalized feedback.

## Project Structure

```
├── app.py              # Main Streamlit app
├── helper.py           # Helper functions (PDF extraction, prompt prep, Gemini API)
├── requirements.txt    # Python dependencies
├── .env                # (Not committed) Your API key
└── README.md           # Project documentation
```

## Technologies Used
- **Python 3.11+**
- **Streamlit** (UI)
- **Google Gemini AI** (Resume analysis)
- **PyPDF2** (PDF text extraction)
- **dotenv** (Environment variable management)

## Acknowledgements
- Google Gemini AI for powerful language analysis
- Streamlit for rapid web app development 
- Streamlit Cloud for hosting