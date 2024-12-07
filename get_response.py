import streamlit as st

import google.generativeai as genai

def start_chat_session():

    # Fetching the API KEY
    genai.configure(api_key=st.session_state["GOOGLE_API_KEY"])

    system_instruction = f"""
    You are an expert resume analyst. I will provide a resume as an image and a job description as text. Your task is to:
    1. Analyze the resume and job description.
    2. Identify key areas in the resume that match the job description.
    3. Suggest specific changes or additions to the resume to better align with the job description.
    4. Provide a match score between the resume and the job description based on relevance and alignment (on a scale of 0 to 100).

    - The match score should be calculated based on the following criteria:
        a. Skills match (40%)
        b. Experience match (30%)
        c. Education/qualifications match (20%)
        d. Other relevant details (10%)

    Provide your analysis in the following format:
    1. Resume Analysis:
        - Key matching areas in the resume:
        - Missing or under-represented elements:
    
    2. Suggested Changes to Resume:
        - [Example: Add skill X that appears in the job description but is missing in the resume]
        - [Example: Rephrase the experience section to better reflect responsibilities mentioned in the job description]

    3. Match Score: [XX/100]
    """
    # Setting model to be used
    model = genai.GenerativeModel("gemini-1.5-flash",
                                system_instruction=system_instruction)

    # starting chat_session
    chat_session = model.start_chat(history=[])

    return chat_session

# Function to convert natural language to SQL
def get_response(input, chat):
    response = chat.send_message(input, stream=True)
    for chunk in response:
        yield chunk.text 