import streamlit as st
from PIL import Image
from datetime import datetime, timedelta
from auth import authenticate_user
from add_event import add_event_to_calendar
from study_timetable import fetch_upcoming_events, create_study_timetable
from streamlit_option_menu import option_menu

# Initialize Streamlit app
st.set_page_config(page_title="AURA Project", page_icon="logo.png", layout="wide")

# Sidebar navigation
st.sidebar.title("AURA Project")
logo = Image.open("logo.png")
st.sidebar.image(logo, caption="AURA: Pembantu Pintar Pembelajaran Peribadi", use_container_width=True)

menu = st.sidebar.radio("Navigate to:", ["Description", "Add Event to Calendar", "Emotion Detection", "Schedule Maker"])

def display_study_timetable():
    st.header("Study Timetable")
    
    st.info("Fetching upcoming events from your Google Calendar...")
    
    try:
        # Fetch upcoming events
        events = fetch_upcoming_events()
        
        if not events:
            st.warning("No upcoming events found!")
            return
        
        # Create study timetable
        timetable = create_study_timetable(events)
        
        if not timetable:
            st.warning("Unable to generate timetable!")
            return
        
        # Display timetable
        for date, tasks in sorted(timetable.items()):
            st.subheader(f"{date.strftime('%A, %d %B %Y')}")
            for task in tasks:
                st.write(f"• {task}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Main content
if menu == "Description":
    st.title("AURA: Pembantu Pintar Pembelajaran Peribadi")
    st.markdown("""
    **AURA** is an innovative project aimed at improving time management and productivity for students.

    - **Add Event to Calendar**: Simplifies event management by integrating with Google Calendar.
    - **Emotion Detection**: Uses real-time face recognition to detect emotions (Coming soon!).
    - **Schedule Maker**: Generates personalized study plans based on upcoming exams and assignments in your Google Calendar.

    Our goal is to provide students with a smarter and more efficient way to plan their daily activities.
    """)

elif menu == "Add Event to Calendar":
    st.title("Add Event to Google Calendar")
    st.markdown("Use the form below to add an event to your Google Calendar.")

    # Input form for adding an event
    with st.form("add_event_form"):
        event_name = st.text_input("Event Name", placeholder="Enter the event name")
        event_date = st.date_input("Event Date")
        event_time = st.time_input("Event Time")
        event_duration = st.number_input("Event Duration (hours)", min_value=1, max_value=12, value=2)
        reminder_minutes = st.number_input("Reminder (minutes before)", min_value=5, max_value=1440, value=60)
        submitted = st.form_submit_button("Add Event")

        if submitted:
            try:
                start_datetime = datetime.combine(event_date, event_time)
                end_datetime = start_datetime + timedelta(hours=event_duration)
                add_event_to_calendar(
                    summary=event_name,
                    description=f"Reminder for {event_name}",
                    start_date=start_datetime,
                    end_date=end_datetime,
                    reminder_minutes=reminder_minutes,
                )
                st.success("Event added successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

elif menu == "Emotion Detection":
    st.title("Emotion Detection")
    st.markdown("This feature is under development. Stay tuned!")

elif menu == "Schedule Maker":
    display_study_timetable()