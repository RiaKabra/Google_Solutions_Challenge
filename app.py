import streamlit as st
import requests
from bs4 import BeautifulSoup
from gemini_utils import recommend_scholarships, generate_sop
from dotenv import load_dotenv
import os
load_dotenv()

CSE_API_KEY = os.getenv("CSE_API_KEY")
CSE_ID = os.getenv("CSE_ID")

def fetch_scholarship_descriptions(student_profile_text):
    search_query = f"scholarships for {student_profile_text} in India 2024 site:buddy4study.com"
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": CSE_API_KEY,
        "cx": CSE_ID,
        "q": search_query,
        "num": 3
    }
    response = requests.get(url, params=params)
    results = response.json()
    descriptions = []
    for item in results.get("items", []):
        link = item.get("link")
        try:
            page = requests.get(link, timeout=5)
            soup = BeautifulSoup(page.content, "html.parser")
            text_parts = []

            text_parts += [p.get_text() for p in soup.find_all('p')[:10]]

            text_parts += [li.get_text() for li in soup.find_all('li')[:15]]

            for table in soup.find_all('table'):
                rows = table.find_all('tr')[:5]
                for row in rows:
                    text_parts.append(row.get_text(separator=' | '))

            text = "\n".join(text_parts)
            descriptions.append(f"{item.get('title')}\n{text}\n{link}")
        except:
            continue
    return "\n---\n".join(descriptions)


st.title("🎓 EduBridge – Real-Time Scholarship Finder")
st.write("Find real scholarships based on your profile using live search + Gemini AI.")

with st.form("student_form"):
    st.subheader("📄 Enter Your Details")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    qualification = st.selectbox("Education Level", ["10th", "12th", "Undergraduate", "Postgraduate"])
    income = st.selectbox("Family Income", ["Upto 1.5L", "1.5L - 3L", "3L - 6L", "Above 6L"])
    percentage = st.selectbox("Academic Score (%)", ["60-70", "70-80", "80-90", "90-100"])
    religion = st.selectbox("Religion", ["Hindu", "Muslim", "Christian", "Sikh", "Other"])
    community = st.selectbox("Community", ["General", "OBC", "SC", "ST", "Other"])
    sports = st.selectbox("Sports Quota", ["Yes", "No"])
    disability = st.selectbox("Disability", ["Yes", "No"])
    exservice = st.selectbox("Ex-Servicemen Quota", ["Yes", "No"])
    goals = st.text_input("Your academic goal (for SOP)", placeholder="e.g. Engineering, Medicine")
    submitted = st.form_submit_button("🔍 Find Scholarships")

if submitted:
    student_profile = f"""
    Gender: {gender}
    Education: {qualification}
    Income: {income}
    Score: {percentage}
    Religion: {religion}
    Community: {community}
    Sports: {sports}
    Disability: {disability}
    Ex-Servicemen: {exservice}
    """

    student_keywords = f"{gender} {community} {qualification} {goals}"

    st.subheader("🎯 Recommended Scholarships (Live)")
    with st.spinner("Searching and scraping scholarship content + matching with Gemini..."):
        scraped_descriptions = fetch_scholarship_descriptions(student_keywords)
        result = recommend_scholarships(student_profile, scraped_descriptions)
    st.markdown(result)

    st.subheader("✍️ Auto-Generated SOP")
    with st.spinner("Generating SOP with Gemini..."):
        sop = generate_sop(goals)
    st.text_area("Your SOP", sop, height=250)
