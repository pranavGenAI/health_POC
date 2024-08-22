import streamlit as st
import PIL.Image
import google.generativeai as genai
import time
import hashlib
import json
import fitz  # PyMuPDF for PDF handling

# Set page title, icon, and dark theme
st.set_page_config(page_title="CAQH Document Classifier: Categorize appeal document", page_icon=">", layout="wide")
st.markdown(
    """
    <style>
    .stButton button {
        background: linear-gradient(120deg,#FF007F, #A020F0 100%) !important;
        color: white !important;
    }
    body {
        color: white;
        background-color: #1E1E1E;
    }
    .stTextInput, .stSelectbox, .stTextArea, .stFileUploader {
        color: white;
        background-color: #2E2E2E;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Configure Google Generative AI with the API key
GOOGLE_API_KEY = "AIzaSyCiPGxwD04JwxifewrYiqzufyd25VjKBkw"
genai.configure(api_key=GOOGLE_API_KEY)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Define users and hashed passwords for simplicity
users = {
    "ankur.d.shrivastav": hash_password("ankur123"),
    "sashank.vaibhav.allu": hash_password("sashank123"),
    "shivananda.mallya": hash_password("shiv123"),
    "pranav.baviskar": hash_password("pranav123")
}

def login():
    col1, col2 = st.columns([0.3, 0.7])  # Create columns
    with col1:
        st.title("Login")
        st.write("Username")
        username = st.text_input("", label_visibility="collapsed")
        st.write("Password")
        password = st.text_input("", type="password", label_visibility="collapsed")
        
        if st.button("Sign in"):
            hashed_password = hash_password(password)
            if username in users and users[username] == hashed_password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid username or password")

def logout():
    # Clear session state on logout
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.success("Logged out successfully!")
    st.rerun()

def extract_text_from_pdf(pdf_file):
    try:
        pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = ""
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

def generate_content(content):
    max_retries = 10
    delay = 10
    retry_count = 0
    while retry_count < max_retries:
        try:
            print("Model definition")
            model = genai.GenerativeModel('gemini-1.5-pro')
            prompt = """You have been given an insurance certificate as input. Now you will help me in extracting the text and return the text.
            1. Name
            2. Policy no
            3. Policy Expiration date
            4. Coverage Limit Amount (in dollars)
            
            Check for the above information and then write the table with data also add rationale in the end. Text : {content}        
            """
            print("Model generate")
            response = model.generate_content([prompt, content], stream=True)
            response.resolve()
            print("Response text", response.text)
            return response.text  # Return generated text
        except Exception as e:
            retry_count += 1
            if retry_count == max_retries:
                st.error(f"Error generating content: Server not available. Please try again later.")
            time.sleep(delay)
    return None

def main():
    st.title("Appeals Classifier")
    col1, col2, col3 = st.columns([4, 1, 4])
    generated_text = ""
    
    with col1:
        uploaded_files = st.file_uploader("Upload appeal summary images or PDFs", type=["jpg", "jpeg", "png", "pdf"], accept_multiple_files=True)
        if uploaded_files:
            for uploaded_file in uploaded_files:
                if uploaded_file.type == "application/pdf":
                    st.write("PDF Uploaded")
                    pdf_text = extract_text_from_pdf(uploaded_file)
                    if pdf_text and st.button(f"Classify Appeal PDF {uploaded_files.index(uploaded_file) + 1}"):
                        with st.spinner("Evaluating..."):
                            generated_text = generate_content(pdf_text)
                else:
                    image = PIL.Image.open(uploaded_file)
                    st.image(image, caption="", use_column_width=True)
                    if st.button(f"Classify Appeal {uploaded_files.index(uploaded_file) + 1}"):
                        with st.spinner("Evaluating..."):
                            generated_text = generate_content(image)
    
    with col3:
        if generated_text:
            st.markdown(
                f"""
                <div class="generated-text-box">
                    <h3>Classification Result:</h3>
                    <p>{generated_text}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown("***")

if __name__ == "__main__":
    if st.session_state.logged_in:
        col1, col2, col3 = st.columns([10, 10, 1.5])
        with col3:
            if st.button("Logout"):
                logout()
        main()
    else:
        login()

# Custom CSS for the header and logo
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Graphik:wght@400;700&display=swap');

    body {
        background-color: #f0f0f0;
        color: black;
        font-family: 'Graphik', sans-serif;
    }
    .main {
        background-color: #f0f0f0;
    }
    .stApp {
        background-color: #f0f0f0;
    }
    header {
        background-color: #660094 !important;
        padding: 10px 40px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .logo {
        height: 30px;
        width: auto;
        margin-right: 20px;
    }
    .header-content {
        display: flex;
        align-items: center;
    }
    .header-right {
        display: flex;
        align-items: center;
    }

    h1 {
        color: black;
        margin: 0;
        padding: 0;
    }

    .generated-text-box {
        border: 3px solid #A020F0;
        padding: 20px;
        border-radius: 10px;
        color: black;
        background-color: #FFFFFF;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <header tabindex="-1" data-testid="stHeader" class="st-emotion-cache-12fmjuu ezrtsby2">
        <div data-testid="stDecoration" id="stDecoration" class="st-emotion-cache-1dp5vir ezrtsby1"></div>
        <div class="header-content">
            <img src="https://www.vgen.it/wp-content/uploads/2021/04/logo-accenture-ludo.png" class="logo" alt="Logo">
        </div>
    </header>
    """,
    unsafe_allow_html=True
)
