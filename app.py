import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

def pdf_to_images(pdf_file):
    # Convert BytesIO object to PDF document
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    images = []

    # Convert each page to an image
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)

    return images

def main():
    st.title("PDF to Image Converter")

    # Upload PDF file
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        # Convert PDF to images
        images = pdf_to_images(uploaded_file)

        # Display each image
        for i, image in enumerate(images):
            st.image(image, caption=f"Page {i + 1}", use_column_width=True)

if __name__ == "__main__":
    main()
