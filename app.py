import streamlit as st
from PIL import Image

from get_response import get_response
from pdf_to_image import pdf_to_image

# Streamlit app

# Title
st.set_page_config(page_title="Resume Optimizer")

# Header
st.title("Resume Optimizer")

# Initializing chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat messages from history on app rerun
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Sidebar for text input and image upload
with st.sidebar.form(key="chat_form", clear_on_submit=True):
    st.header("Resume Upload")
    # Get resume input from user
    file_object = st.file_uploader("Maximum 5 Pages if PDF", type=["pdf", "jpg", "jpeg", "png"], help="Max 5 Pages, if PDF")
    # Get job description
    job_desc = st.text_input(label="Job Description", placeholder="Paste your job description here")
    # Submit Button
    submit_file = st.form_submit_button("Optimize")

text = st.chat_input(placeholder="Get more insights.")

# React to user input
if submit_file or text:
        input = []
        # If prompt has a file attachment
        if submit_file and file_object and job_desc:
            with st.spinner("Processing your resume..."):
                # If file is an image
                if file_object.type[-3:] != "pdf":
                    # Extract image file from the attached file_object
                    file = Image.open(file_object)
                    input.append(file)
                # If file is a pdf:
                else:
                    image_list = pdf_to_image(file_object)
                    for image in image_list:
                        input.append(image)

            input.append("Job Desciption:\n\n" + job_desc)
            # Display user message in chat message container
            st.chat_message("assistant").markdown(f"Resume Processed Successfully")
    
        # If prompt is only text
        if text:
            # Content to be given to Model
            input.append(text)
            # Display user message in chat message container
            st.chat_message("user").markdown(text)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": text})

        if input:
                with st.spinner(text="Analysing Resume..."):
                    # Display assistant response in chat message container
                    response = st.chat_message("assistant").write_stream(stream=get_response(input))
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})