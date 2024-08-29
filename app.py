import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import google.generativeai as genai
import time  # Import time module for sleep function

GOOGLE_API_KEY = "AIzaSyCiPGxwD04JwxifewrYiqzufyd25VjKBkw"
genai.configure(api_key=GOOGLE_API_KEY)
text = """
        1. Name:
        2. Policy no:
        3. Policy Expiration date:
        4. Coverage Limit Amount (in dollar):"""
dict_ = ""
def generate_content(image):
    max_retries = 10
    delay = 10
    retry_count = 0
    while retry_count < max_retries:
        try:
            # Initialize the GenerativeModel
            print("Model definition")
            model = genai.GenerativeModel('gemini-1.5-pro')
            prompt = """Extract only the below information from the image. If some of the below information is not present in the image then keep it blank. 
            {dict_}       
            Output should be in json format with only Name, Policy no, Policy Expiration date, Coverage Limit Amount (in dollar) as key.
            """
            # Generate content using the image
            print("Model generate")
            response = model.generate_content([prompt, image], stream=True)
            response.resolve()
            dict_ = response.text        
            #st.write("Response text", response.text)        
            return none  # Return generated text
        except Exception as e:
            retry_count += 1
            if retry_count == max_retries:
                st.error(f"Error generating content: Server not available. Please try again after sometime")
            time.sleep(delay)
    
    # Return None if all retries fail
    return None


def pdf_to_images(pdf_file):
    # Open the PDF file
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    
    for page_number in range(len(pdf_document)):
        # Get a page
        page = pdf_document.load_page(page_number)
        # Render page to a pixmap
        pix = page.get_pixmap()
        
        # Convert pixmap to PIL Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        generate_content(img)
        
    return text

def main():
    st.title("PDF to PNG Converter")
    
    # Upload PDF file
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if pdf_file:
        # Convert PDF pages to images and extract text
        text = pdf_to_images(pdf_file)        
        st.write(dict_)  # Write only the last output

if __name__ == "__main__":
    main()
