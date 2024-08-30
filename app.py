import streamlit as st
import pandas as pd
import io
import google.generativeai as genai

# Initialize Google Gemini API
GOOGLE_API_KEY = "AIzaSyCiPGxwD04JwxifewrYiqzufyd25VjKBkw"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

def classify_text(text):
    prompt = f"""Analyze the text and classify it into either of the below categories: GenAI Strategy & Adoption, AI Strategy & Data Governance, Data Analytics & Reporting, AI Polity & Responsible AI

Text to classify: {text}

only return the classification category only"""
    
    response = model.generate_content(prompt)
    return response.text.strip()

def main():
    st.title('Excel File Classifier')

    uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")
    if uploaded_file is not None:
        # Load the Excel file
        df = pd.read_excel(uploaded_file)

        # Check if column A exists
        if 'A' not in df.columns:
            st.error("Column A is missing in the uploaded file.")
            return

        if st.button('Classify Text'):
            # Scan Column A and classify
            df['B'] = df['A'].apply(lambda x: classify_text(x))
            
            # Save the updated DataFrame to a new Excel file
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
            
            output.seek(0)
            st.download_button(
                label="Download Updated Excel File",
                data=output,
                file_name="classified_texts.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

if __name__ == "__main__":
    main()
