import streamlit as st
from PIL import Image
from datetime import datetime, timedelta
from auth import authenticate_user
from add_event import add_event_to_calendar, submit_event
from study_timetable import fetch_upcoming_events, create_study_timetable, display_study_timetable
from emotion_utils import detect_emotion, get_recommendation, provide_feedback, display_emotion_feedback
from streamlit_option_menu import option_menu
from chatbot import chat_bot
import google.generativeai as ai
import os

# Configure the API Key
GENAI_API_KEY = st.secrets["GENAI_API_KEY"]
if not GENAI_API_KEY:
    raise ValueError("API Key not found! Please set GOOGLE_GENAI_API_KEY.")

ai.configure(api_key=GENAI_API_KEY)

# Initialize Streamlit app
st.set_page_config(page_title="AURA Project", page_icon="logo.png", layout="wide")

# Sidebar navigation
logo = Image.open("logo.png")
st.sidebar.image(logo, use_container_width=True)

# Sidebar configuration
with st.sidebar:
    selected_section = option_menu(
        menu_title="Main",  # Title of the sidebar menu
        options=[
            "AURA Home",
            "Test Our Product",
        ],  # Menu options
        icons=[
            "house",
            "person-fill",
        ],  # Menu icons (use https://icons.getbootstrap.com/)
        menu_icon="list",  # Icon for the sidebar menu
        default_index=0,  # Default selected item
        styles={
            "menu_title": {"font-size": "15px"},
            "container": {"padding": "5px", "background-color": "#000000"},
            "icon": {"color": "white", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "5px",
                "--hover-color": "#e2d7f4",
            },
            "nav-link-selected": {"background-color": "#ac94f4"},
        },
    )

# Section routing based on selection
if selected_section == "AURA Home":
    st.title("AURA: Pembantu Pintar Pembelajaran Peribadi")
    st.markdown("""
    **AURA** is an innovative project aimed at improving time management and productivity for students.

    - **Add Event to Calendar**: Simplifies event management by integrating with Google Calendar.
    - **Emotion Detection**: Uses real-time face recognition to detect emotions (Coming soon!).
    - **Schedule Maker**: Generates personalized study plans based on upcoming exams and assignments in your Google Calendar.

    Our goal is to provide students with a smarter and more efficient way to plan their daily activities.
    """)

elif selected_section == "Test Our Product":
    choice = st.selectbox("Select Functions:",["None","Emotion Detection","Add Event","Create Timetable","Chatbot"])

    if choice == "Add Event":
        st.title("Add Event to Google Calendar")
        st.markdown("Use the form below to add an event to your Google Calendar.")
        submit_event()
    
    if choice == "Emotion Detection":
        st.header("Emotion Detection")
        if st.button("Start Emotion Detection"):
            st.write("Press 'q' to stop detection.")
            detected_emotion = detect_emotion()
            display_emotion_feedback(detected_emotion)
            provide_feedback(detected_emotion)

    if choice == "Create Timetable":
        st.header("Create Timetable")
        if st.button("Create a Study Timetable"):
            display_study_timetable()

    if choice == "Chatbot":
        st.header("AI Chatbot")
        st.write("Interact with the AURA Chatbot below:")
        chat_bot()