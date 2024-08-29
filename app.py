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
    text =""
    for page_number in range(len(pdf_document)):
        # Get a page
        page = pdf_document.load_page(page_number)
        # Render page to a pixmap
        pix = page.get_pixmap()
        
        # Convert pixmap to PIL Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
        
        # Generate content using the image
        prompt = """If the some of the below information is not present in the image then keep it blank. You just need to fill in the blanks in the {text}, if you can find the information from the image. 
        1. Name:
        2. Policy no:
        3. Policy Expiration date:
        4. Coverage Limit Amount (in dollar):
        """
        print("Generating content...")
        response = model.generate_content([prompt, img], stream=True)  # Ensure correct usage as per documentation
        response.resolve()
        text += response.text
        print(text)
        
    st.write(text)
    return text

def process_text_in_chunks(text, chunk_size=5000):
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks


def extract_information_from_text(text):
    model = genai.GenerativeModel("gemini-1.5-pro")
    prompt_template = """
    
    Text: {text}
    """
    
    consolidated_result = ""
    for chunk in process_text_in_chunks(text):
        prompt = prompt_template.format(text=chunk)
        response = model.generate_content(prompt, stream=True)
        response.resolve()
        consolidated_result += response.text
    
    prompt_template_2 = """
    You have been given the text and now extract the following information:
    1. Name
    2. Policy no
    3. Policy Expiration date
    4. Coverage Limit Amount (in dollar)

    Text: {consolidated_result}
    """
    response = model.generate_content(prompt, stream=True)
    response.resolve()
    return response.text


def main():
    st.title("PDF to PNG Converter")
    
    # Upload PDF file
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if pdf_file:
        # Convert PDF pages to images and extract text
        text = pdf_to_images(pdf_file)
        
        # Process the text to extract relevant information
        st.write("*******************************")
        
        #extracted_info = extract_information_from_text(text)
        #st.write(extracted_info)


if __name__ == "__main__":
    main()
