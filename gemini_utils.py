
import requests  
import json  
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
HEADERS = {"Content-Type": "application/json"}  

def call_gemini(prompt):  
    body = {  
        "contents": [  
            {  
                "role": "user",  
                "parts": [{"text": prompt}]  
            }  
        ]  
    }  

    response = requests.post(API_URL, headers=HEADERS, data=json.dumps(body))  

    if response.status_code == 200:  
        try:  
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]  
        except:  
            return "⚠️ Gemini did not return expected content."  
    else:  
        return f"❌ Error {response.status_code} — {response.text}"  


def recommend_scholarships(student_profile, scholarships_list):  
    prompt = f"""  
You are an AI assistant that helps students find scholarships.

Student Profile:
{student_profile}

Here is a list of available scholarships:
{scholarships_list}

Recommend the top 3 scholarships that are most relevant to this student. Explain why each one matches.
"""  
    return call_gemini(prompt)  


def generate_sop(student_goal):  
    prompt = f"""  
Write a 200-word Statement of Purpose for a student from a low-income background who is passionate about {student_goal}. 
The student has good grades and wants to serve the community. The tone should be humble, confident, and inspiring.
"""  
    return call_gemini(prompt)
