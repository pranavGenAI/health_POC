import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

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
