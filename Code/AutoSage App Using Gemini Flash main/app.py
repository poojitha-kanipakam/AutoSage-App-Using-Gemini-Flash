# -------------------- IMPORT LIBRARIES --------------------
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import base64

# -------------------- CONFIGURE GEMINI API --------------------
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="AutoSage", page_icon="🚗", layout="centered")

# -------------------- ADD LOCAL BACKGROUND IMAGE(Optional) --------------------
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)),
                    url("data:image/jpeg;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    h1 {{
        text-align: center;
        font-size: 40px;
        color: #ffffff;
        letter-spacing: 1px;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.8);
    }}

    h2, h3, p, div, label {{
        color: #ffffff !important;
    }}

    /* Button styling */
    .stButton>button {{
        background-color: #ff4b4b;
        color: white;
        font-size: 18px;
        border-radius: 12px;
        height: 3em;
        width: 100%;
        border: none;
        transition: 0.3s ease;
    }}

    .stButton>button:hover {{
        background-color: #ff1f1f;
        box-shadow: 0 0 15px rgba(255,75,75,0.7);
        transform: scale(1.03);
    }}

    /* File uploader */
    .stFileUploader {{
        background-color: rgba(255,255,255,0.12);
        padding: 12px;
        border-radius: 12px;
    }}

    </style>
    """, unsafe_allow_html=True)

add_bg_from_local("background.jpg")

# -------------------- GEMINI RESPONSE FUNCTION --------------------
def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    response = model.generate_content([input_prompt, image[0]])
    return response.text

# -------------------- IMAGE SETUP FUNCTION --------------------
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# -------------------- GEMINI PROMPT --------------------
input_prompt = """
You are an automobile expert tasked with providing a detailed overview of any vehicles.
Provide structured output:

Brand:
Model:
Launch year:
Key Features (Top 3):
Mileage (km/l):
Average Price in INR:
Other Details:
Approximate Resale Value after 10 years:
"""

# -------------------- UI --------------------
st.title("🚗 AutoSage - AI Vehicle Expert")

st.write("Upload a vehicle image and get detailed AI-powered insights instantly!")

uploaded_file = st.file_uploader("📸 Upload Vehicle Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Vehicle Image", use_column_width=True)

submit = st.button("🚀 Get Vehicle Details")

if submit:
    if uploaded_file is not None:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data)

        st.success("✅ Vehicle Analysis Completed!")
        st.subheader("📋 Vehicle Details:")
        st.write(response)
    else:
        st.error("⚠ Please upload an image first!")