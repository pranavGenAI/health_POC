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
    images = []

    model = genai.GenerativeModel('gemini-1.5-pro')
    
    for page_number in range(len(pdf_document)):
        # Get a page
        page = pdf_document.load_page(page_number)
        # Render page to a pixmap
        pix = page.get_pixmap()
        
        # Convert pixmap to PIL Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
        
        # Generate content using the image
        prompt = "Extract the text from the image and write it."
        print("Generating content...")
        response = model.generate_content([prompt, img], stream=True)  # Ensure correct usage as per documentation
        response.resolve()
        st.write("Response text", response.text)
        
    return images


def main():
    st.title("PDF to PNG Converter")
    
    # Upload PDF file
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if pdf_file:
        # Convert PDF pages to images
        images = pdf_to_images(pdf_file)
        

if __name__ == "__main__":
    main()
