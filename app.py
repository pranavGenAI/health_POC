import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

def pdf_to_images(pdf_file):
    # Open the PDF file
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    images = []

    for page_number in range(len(pdf_document)):
        # Get a page
        page = pdf_document.load_page(page_number)
        # Render page to an image
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Save image to a BytesIO object
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        images.append(img_byte_arr.getvalue())

    return images

def main():
    st.title("PDF to PNG Converter")
    
    # Upload PDF file
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if pdf_file:
        # Convert PDF pages to images
        images = pdf_to_images(pdf_file)
        
        # Display each image
        for i, img_data in enumerate(images):
            st.image(img_data, caption=f'Page {i+1}', use_column_width=True)

if __name__ == "__main__":
    main()
