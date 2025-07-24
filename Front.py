import streamlit as st
import subprocess
import sys
import os

def main():
    
    st.set_page_config(
        page_title="Drowsiness Detection App",
        page_icon="🚗",
        layout="centered"
    )
    
    
    st.markdown("""
    <style>
    .main-container {
        background-color: #0D1117;
        color: #FFFFFF;
        padding: 30px;
        border-radius: 10px;
        text-align: center;
    }
    .logo-text {
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .tagline {
        font-size: 24px;
        color: #58A6FF;
        margin-bottom: 20px;
    }
    .intro-text {
        font-size: 18px;
        color: #C9D1D9;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)
    

    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    
    st.markdown('<div class="logo-text">🚗 Drowsiness Detection App</div>', unsafe_allow_html=True)
    

    st.markdown('<div class="tagline">Stay Alert, Stay Safe!</div>', unsafe_allow_html=True)
    
    
    st.markdown(
        '<div class="intro-text">This app helps detect drowsiness while driving and guides you to the nearest rest stop when needed.</div>', 
        unsafe_allow_html=True
    )
    
    # Start Detection Button
    if st.button("🟢 Start Detection", key="start_detection", use_container_width=True):
        try:
            # Create a file to signal detection start
            with open('start_detection.flag', 'w') as f:
                f.write('start')
            
            st.success("Drowsiness detection started. Camera will open shortly.")
        except Exception as e:
            st.error(f"Error starting detection: {e}")
    
    
    st.markdown(
        '<div class="footer">' + 
        '<p>Privacy Disclaimer: No personal data is stored. Drive safe!</p>' +
        '<p>Powered by OpenCV & Python</p>' +
        '</div>', 
        unsafe_allow_html=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
