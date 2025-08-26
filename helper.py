import google.generativeai as genai
import PyPDF2 as pdf
import json
import os

def configure_genai(api_key):
    genai.configure(api_key=api_key)
    
def extract_pdf_text(file):
    try:
        reader = pdf.PdfReader(file)
        if len(reader.pages) == 0:
            raise Exception("Uploaded file is empty")

        text = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
        if not text:
            raise Exception("No text could be extracted from the uploaded file")
        
        return " ".join(text)
    
    except Exception as e:
        raise Exception(f"Error extracting PDF text: {e}")

def prepare_prompt(text, jd):
    if not text or not jd:
        raise ValueError("Resume and/or job description must be provided")
    
    prompt_template = """
    Act as an expert ATS (Application Tracking System) specialist with deep expertise in:
    - Technical fields
    - Resume screening
    - Candidate evaluation
    - Job matching
    - Interview processes
    - Software Engineering
    - Data Science, Analytics and Engineering
    - Artificial Intelligence
    - Machine Learning 
    
    Evaluate the following resume against the job description. Consider that the job market is highly competitive. Provide detailed feedback for resume improvement.

    Resume:
    {text}

    Job Description:
    {jd}

    Provide the response in the following JSON format ONLY:
    {{
        "JD Match": "percentage between 0-100",
        "Missing Keywords": "list of missing keywords from the job description",
        "Profile Summary": "brief summary of the candidate's profile and also provide a detailed feedback for improvement in a new paragraph",
    }}
    """
    
    return prompt_template.format(text=text.strip(), jd=jd.strip())

def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        
        if not response or not response.text:
            raise Exception("Received empty response from Gemini API")
        
        try:
            response_json = json.loads(response.text)
            required_fields = ["JD Match", "Missing Keywords", "Profile Summary"]
            for i in required_fields:
                if i not in response_json:
                    raise ValueError(f"Missing field in response: {i}")
                
            return response.text
        
        except json.JSONDecodeError:
            import re
            json_pattern = r'\{.*\}'
            match = re.search(json_pattern, response.text, re.DOTALL)
            if match:
                return match.group()
            else:
                raise ValueError("Response is not valid JSON and no JSON object found in the text")
            
    except Exception as e:
        raise Exception(f"Error parsing JSON response: {str(e)}")
        