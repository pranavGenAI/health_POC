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
        # Save image to a BytesIO object
        img_byte_arr = io.BytesIO()
        pix.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)  # Reset the stream position to the beginning
        
        # Open image using PIL.Image.open
        img = Image.open(img_byte_arr)
        images.append(img)

    return images

def main():
    st.title("PDF to PNG Converter")
    
    # Upload PDF file
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if pdf_file:
        # Convert PDF pages to images
        images = pdf_to_images(pdf_file)
        
        # Display each image
        for i, img in enumerate(images):
            st.image(img, caption=f'Page {i+1}', use_column_width=True)

if __name__ == "__main__":
    main()
