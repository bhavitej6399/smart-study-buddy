import streamlit as st
import ssl
import os
import easyocr
import numpy as np
from PIL import Image
from openai import OpenAI

st.title("📚 Smart Study Buddy")
st.write("Upload your handwritten notes to generate a quiz!")

# Setup OCR and AI
reader = easyocr.Reader(['en'])
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

uploaded_file = st.file_uploader("Choose a photo of your notes", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Show the image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Notes", use_container_width=True)
    
    if st.button("✨ Generate Quiz"):
        with st.spinner("Reading notes and thinking..."):
            # 1. OCR: Extract text
            img_array = np.array(image)
            text_results = reader.readtext(img_array, detail=0)
            raw_text = " ".join(text_results)
            
            # 2. AI: Generate Quiz
            prompt = f"Based on these study notes, create a 3-question multiple choice quiz with an answer key at the bottom:\n\n{raw_text}"
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            
            # 3. Display Result
            st.subheader("📝 Your Personalized Quiz")
            st.write(response.choices[0].message.content)
