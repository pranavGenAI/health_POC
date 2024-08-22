import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import google.generativeai as genai

# Configure the Google Generative AI API
GOOGLE_API_KEY = "AIzaSyCiPGxwD04JwxifewrYiqzufyd25VjKBkw"
genai.configure(api_key=GOOGLE_API_KEY)

def pdf_to_images(pdf_file):
    # Convert BytesIO object to PDF document
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    images = []

    # Convert each page to an image and save as PNG
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Save image as PNG in a BytesIO buffer
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        
        # Create a PIL Image object from the buffer
        img_pil = Image.open(buffer)
        
        # Convert the PIL image to a format acceptable by the API
        img_buffer = io.BytesIO()
        img_pil.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        # Initialize the Google Gemini model
        model = genai.GenerativeModel('gemini-1.5-pro')
        prompt = "Extract the text from this image and return only that."
        
        # Generate content using the image
        print("Model generate")
        response = model.generate_content([prompt, img_buffer], stream=True)
        response.resolve()
        
        st.write(f"Response text for Page {page_num + 1}:", response.text)
        
        # Add the PNG image buffer to the list
        images.append(buffer)

    return images

def main():
    st.title("PDF to Image Converter")

    # Upload PDF file
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        # Convert PDF to images
        images = pdf_to_images(uploaded_file)

        # Display each image
        for i, img_buffer in enumerate(images):
            st.image(img_buffer, caption=f"Page {i + 1}", use_column_width=True)

if __name__ == "__main__":
    main()
