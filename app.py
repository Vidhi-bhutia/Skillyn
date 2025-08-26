import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import os
import json
from dotenv import load_dotenv
from helper import configure_genai, extract_pdf_text, prepare_prompt, get_gemini_response

def set_custom_style():
    st.markdown("""
        <style>
        /* Background Gradient */
        .stApp {
            background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
        }

        /* Dark Mode Adaptation */
        @media (prefers-color-scheme: dark) {
            .stApp {
                background: linear-gradient(135deg, #1f1f1f, #2c2c2c);
                color: #f0f0f0;
            }
        }

        /* Title Styling */
        h1 {
            text-align: center;
            font-size: 2.8em !important;
            background: -webkit-linear-gradient(#00c6ff, #0072ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
        }

        /* Subheading Styling */
        h2, h3 {
            color: #0072ff !important;
            margin-top: 25px;
        }

        /* Metrics Styling */
        [data-testid="stMetric"] {
            background: rgba(0, 114, 255, 0.1);
            border-radius: 15px;
            padding: 10px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
        }

        /* Button Styling */
        .stButton button {
            background: linear-gradient(135deg, #0072ff, #00c6ff);
            color: white;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
            padding: 10px 20px;
            transition: 0.3s;
        }
        .stButton button:hover {
            background: linear-gradient(135deg, #00c6ff, #0072ff);
            transform: scale(1.05);
        }

        /* Card-like boxes for results */
        .card {
            background: rgba(255,255,255,0.8);
            border-radius: 12px;
            padding: 15px;
            margin: 10px 0;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
        }
        @media (prefers-color-scheme: dark) {
            .card {
                background: rgba(30,30,30,0.9);
                box-shadow: 0px 4px 15px rgba(255,255,255,0.05);
            }
        }
        </style>
    """, unsafe_allow_html=True)


def init_session_state():
    if 'processing' not in st.session_state:
        st.session_state.processing = False


def main():
    load_dotenv()
    init_session_state()
    set_custom_style()
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("API key not found. Please set the GOOGLE_API_KEY environment variable.")
        return
    
    try:
        configure_genai(api_key)
    except Exception as e:
        st.error(f"Error configuring Google Generative AI: {e}")
        return
    
    with st.sidebar:
        st.title("Skillyn")
        st.write("Your **Smart ATS Tool** to:")
        st.markdown("""
        - ✅ Evaluate resume-job match  
        - ✅ Extract key skills  
        - ✅ Gives feedback for improvement  
        """)
        
        st.markdown("---")
        st.subheader("Know the Creator")
        st.markdown("""
        **Vidhi Bhutia**  
        """)
        st.markdown(
            """
            <div class="sidebar-links">
            <a href="https://www.linkedin.com/in/vidhibhutia" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/145/145807.png" height=25px> LinkedIn
            </a><br>
            <a href="https://github.com/Vidhi-bhutia" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/733/733553.png" height=25px> GitHub
            </a>
            </div>
            """, unsafe_allow_html=True)

    st.title("Skillyn - Smart ATS Resume Analyzer")
    st.subheader("Upload Resume and Job Description to Get Started")

    jd = st.text_area("📄 Paste Job Description Here", height=200)
    file = st.file_uploader("📑 Upload Resume (PDF only)", type=["pdf"])

    if st.button("🚀 Analyze"):
        if not jd or not file:
            st.warning("⚠️ Please provide both a job description and a resume.")
            return
        
        with st.spinner("🔍 Processing your resume..."):
            pdf_text = extract_pdf_text(file)
            prompt = prepare_prompt(pdf_text, jd)
            response = get_gemini_response(prompt)
            response_json = json.loads(response)
            
            st.session_state.processing = False

            if response_json:
                st.success("✅ Analysis Complete!")
                st.metric("Job Description Match", f"{response_json.get('JD Match', 0)}%")
                
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("Missing Keywords")
                missing_keywords = response_json.get("Missing Keywords", [])
                st.write(", ".join(missing_keywords) if missing_keywords else "No critical missing keywords found.")
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("Profile Summary & Improvement points")
                st.write(response_json.get("Profile Summary", "No profile summary found."))
                st.markdown('</div>', unsafe_allow_html=True)
                
            else:
                st.error("❌ Error analyzing resume.")


if __name__ == "__main__":
    main()

