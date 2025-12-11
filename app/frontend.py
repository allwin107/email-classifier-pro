import streamlit as st
import requests
import os
from dotenv import load_dotenv

# 1. Page Setup (MUST BE THE FIRST STREAMLIT COMMAND)
st.set_page_config(page_title="Enterprise Email AI", page_icon="🛡️")

# 2. Load Environment Variables
load_dotenv() # This looks for the .env file

# 3. Get Configuration
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")

# 4. Critical Safety Check
if not API_URL or not API_KEY:
    st.error("⚠️ System Error: Secrets not found.")
    st.info("Please verify you have a '.env' file in your project folder with API_URL and API_KEY.")
    st.stop() # Stop execution here so the app doesn't crash later

# 5. UI Layout
st.title("🛡️ Enterprise PII & Classification System")
st.markdown("---")

# Sidebar for status
with st.sidebar:
    st.header("System Status")
    try:
        # We add a generic timeout so it doesn't freeze
        response = requests.get(f"{API_URL}/", timeout=2)
        if response.status_code == 200:
            st.success("✅ API Online")
        else:
            st.error("❌ API Offline")
    except Exception:
        st.error("❌ Connection Failed")
    
    st.caption(f"Connected to: {API_URL}")

# Main Input Area
st.subheader("Analyze Incoming Email")
email_text = st.text_area("Paste the email content here:", height=200, placeholder="Example: My laptop screen is broken...")

# The Action Button
if st.button("🚀 Classify & Protect", type="primary"):
    if not email_text:
        st.warning("Please enter some text first.")
    else:
        with st.spinner("Encrypting PII and analyzing context..."):
            try:
                payload = {"text": email_text}
                # We send the secure key in the header
                headers = {"Authorization": f"Bearer {API_KEY}"}
                
                response = requests.post(f"{API_URL}/classify", json=payload, headers=headers)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.success("Analysis Complete!")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Category", result['category'])
                    with col2:
                        conf = result['confidence_score']
                        color = "normal"
                        if conf < 0.5: color = "off"
                        st.metric("Confidence Score", f"{conf*100:.1f}%", delta_color=color)

                    st.markdown("### 🔒 Secure Masked Output")
                    st.code(result['masked_text'], language="text")
                    
                    with st.expander("View Raw JSON Response"):
                        st.json(result)
                        
                elif response.status_code == 403:
                    st.error("⛔ Access Denied: Incorrect API Key in .env file.")
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
                    
            except Exception as e:
                st.error(f"Connection Error: {e}")

st.markdown("---")
st.caption("Enterprise Security System v1.0")