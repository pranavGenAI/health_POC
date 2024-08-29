import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyCiPGxwD04JwxifewrYiqzufyd25VjKBkw"
genai.configure(api_key=GOOGLE_API_KEY)


def pdf_to_images(pdf_file):
    # Open the PDF file
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    text = ""
    
    for page_number in range(len(pdf_document)):
        # Get a page
        page = pdf_document.load_page(page_number)
        # Render page to a pixmap
        pix = page.get_pixmap()
        
        # Convert pixmap to PIL Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Generate content using the image
        prompt = """Extract below information from the image. If some of the below information is not present in the image then keep it blank. You just need to fill in the blanks in the {text}, if you can find the information from the image. 
        1. Name:
        2. Policy no:
        3. Policy Expiration date:
        4. Coverage Limit Amount (in dollar):
        """
        
        max_retries = 10
        for attempt in range(max_retries):
            try:
                print("Generating content...")
                response = model.generate_content([prompt, img], stream=True)  # Ensure correct usage as per documentation
                response.resolve()
                text = response.text
                break  # Exit loop if successful
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    st.error(f"Failed to generate content after {max_retries} attempts.")
    
    return text

def main():
    st.title("PDF to PNG Converter")
    
    # Upload PDF file
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if pdf_file:
        # Convert PDF pages to images and extract text
        text = pdf_to_images(pdf_file)        
        st.write(text)  # Write only the last output

if __name__ == "__main__":
    main()
