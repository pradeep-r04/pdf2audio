import streamlit as st
import PyPDF2
import io
from gtts import gTTS
import pygame
import os
import time

# Streamlit App Title
st.title("📄 PDF to Speech Converter 🔊")

# Initialize session state variables
if "audio_playing" not in st.session_state:
    st.session_state.audio_playing = False
if "current_position" not in st.session_state:
    st.session_state.current_position = 0  # Start from beginning
if "reset_flag" not in st.session_state:
    st.session_state.reset_flag = False

# Function to play speech
def play_speech(text, resume=False):
    # Stop existing playback
    if st.session_state.audio_playing:
        pygame.mixer.music.stop()
        pygame.mixer.quit()  # Fully unload pygame to release file

    # Ensure old file is deleted
    if os.path.exists("speech.mp3"):
        try:
            os.remove("speech.mp3")
            time.sleep(1)  # Wait for the file to be unlocked
        except PermissionError:
            st.error("Error: Could not delete previous audio file. Please try again.")

    # Convert text to speech and save as MP3
    tts = gTTS(text=text, lang="en")
    tts.save("speech.mp3")

    # Initialize pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load("speech.mp3")

    # If resuming, start from last stopped position
    if resume and st.session_state.current_position > 0:
        pygame.mixer.music.play(start=st.session_state.current_position)
    else:
        pygame.mixer.music.play()

    st.session_state.audio_playing = True

# Function to stop speech
def stop_speech():
    if st.session_state.audio_playing:
        st.session_state.current_position = pygame.mixer.music.get_pos() / 1000  # Save position in seconds
        pygame.mixer.music.stop()
        pygame.mixer.quit()  # Unload pygame to release file lock
        st.session_state.audio_playing = False
        st.warning("Reading stopped.")

# Function to reset speech
def reset_speech():
    stop_speech()  # Stop any ongoing playback
    st.session_state.reset_flag = True  # Set reset flag
    st.session_state.current_position = 0  # Reset position
    pygame.mixer.quit()  # Unload pygame to ensure file is not locked
    st.success("Reading reset. Click 'Start Reading' to begin from the start.")

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file:
    # Convert file to a stream
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
    total_pages = len(pdf_reader.pages)

    # Select page range
    start_page = st.number_input("Start Page", min_value=1, max_value=total_pages, value=1)
    end_page = st.number_input("End Page", min_value=start_page, max_value=total_pages, value=total_pages)

    # Extract text
    extracted_text = ""
    for num in range(start_page - 1, end_page):
        page = pdf_reader.pages[num]
        extracted_text += page.extract_text() + "\n\n"

    # Display Extracted Text
    st.text_area("Extracted Text", extracted_text, height=300)

    # Convert to Speech Buttons
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🔊 Start Reading"):
            if extracted_text.strip():
                play_speech(extracted_text)
            else:
                st.error("No text found in the selected pages!")

    with col2:
        if st.button("⏸ Stop Reading"):
            stop_speech()

    with col3:
        if st.button("▶️ Resume Reading"):
            if not st.session_state.audio_playing and st.session_state.current_position > 0:
                play_speech(extracted_text, resume=True)
            else:
                st.error("No paused reading to resume!")

    with col4:
        if st.button("🔄 Reset Reading"):
            reset_speech()

# Streamlit Footer
st.markdown("---")
st.markdown("💡 Developed by PRADEEP SINGH, for more visit https://github.com/pradeep-r04")


st.markdown("---")  # Adds a horizontal line
st.markdown("### Connect with me:")
st.markdown("""
    <hr>
    <div style="text-align: center;">
        <a href="https://www.linkedin.com/in/pradeep-singh4" target="_blank" style="margin-right: 15px;">
            <img src="https://img.icons8.com/fluent/48/000000/linkedin.png"/>
        </a>
        <a href="https://github.com/pradeep-r04" target="_blank" style="margin-right: 15px;">
            <img src="https://img.icons8.com/fluent/48/000000/github.png"/>
        </a>
        <a href="https://twitter.com/altpradeep" target="_blank" style="margin-right: 15px;">
            <img src="https://img.icons8.com/ios-filled/48/ffffff/x.png" width="40" style="background: black; border-radius: 8px; padding: 5px;"/>
        </a>
        <a href="https://instagram.com/whypradeeep" target="_blank">
            <img src="https://img.icons8.com/fluent/48/000000/instagram-new.png"/>
        </a>
    </div>
""", unsafe_allow_html=True)

