import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyCiPGxwD04JwxifewrYiqzufyd25VjKBkw"
genai.configure(api_key=GOOGLE_API_KEY)

def extract_information_from_image(img, model):
    prompt = """If some of the below information is not present in the image then keep it blank. You just need to fill in the blanks in the {text}, if you can find the information from the image. 
    1. Name:
    2. Policy no:
    3. Policy Expiration date:
    4. Coverage Limit Amount (in dollar):
    """
    
    max_retries = 5
    for attempt in range(max_retries):
        try:
            print("Generating content...")
            response = model.generate_content([prompt, img], stream=True)  # Ensure correct usage as per documentation
            response.resolve()
            return response.text
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                st.error(f"Failed to generate content after {max_retries} attempts.")
    return ""

def pdf_to_images(pdf_file):
    # Open the PDF file
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    final_info = {
        "Name": "",
        "Policy no": "",
        "Policy Expiration date": "",
        "Coverage Limit Amount (in dollar)": ""
    }
    
    for page_number in range(len(pdf_document)):
        # Get a page
        page = pdf_document.load_page(page_number)
        # Render page to a pixmap
        pix = page.get_pixmap()
        
        # Convert pixmap to PIL Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Extract information from the image
        page_info = extract_information_from_image(img, model)
        
        # Update final_info with the page_info
        for line in page_info.splitlines():
            if line.startswith("1. Name:"):
                final_info["Name"] = line.split(":", 1)[1].strip()
            elif line.startswith("2. Policy no:"):
                final_info["Policy no"] = line.split(":", 1)[1].strip()
            elif line.startswith("3. Policy Expiration date:"):
                final_info["Policy Expiration date"] = line.split(":", 1)[1].strip()
            elif line.startswith("4. Coverage Limit Amount (in dollar):"):
                final_info["Coverage Limit Amount (in dollar)"] = line.split(":", 1)[1].strip()

    return final_info

def main():
    st.title("PDF to PNG Converter")
    
    # Upload PDF file
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if pdf_file:
        # Convert PDF pages to images and extract information
        final_info = pdf_to_images(pdf_file)        
        st.write("Information extracted from PDF:")
        st.write(f"1. Name: {final_info['Name']}")
        st.write(f"2. Policy no: {final_info['Policy no']}")
        st.write(f"3. Policy Expiration date: {final_info['Policy Expiration date']}")
        st.write(f"4. Coverage Limit Amount (in dollar): {final_info['Coverage Limit Amount (in dollar)']}")

if __name__ == "__main__":
    main()
