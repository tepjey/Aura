import streamlit as st
from datetime import datetime
import google.generativeai as ai

def chat_bot():
    # Initialize chat history if not already in session_state
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Sidebar: Clear Chat Button
        if st.sidebar.button("Clear Chat"):
            st.session_state.chat_history = []  # Clear chat history
            st.success("Chat history cleared!")

        # Input box for user query
        with st.form("chatbot_form"):
            user_message = st.text_input("You:", key="user_message")
            submitted = st.form_submit_button("Send")

        # Process user input and update chat history
        if submitted and user_message:
            try:
                # Initialize the chatbot model
                model = ai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=(
                        "You are AURA, an intelligent assistant designed to help users manage their studies, "
                        "plan schedules, and improve productivity. You provide polite, concise, and accurate "
                        "responses. Your tasks include creating study timetables, offering real-time feedback based "
                        "on user emotions, and assisting with event scheduling. Use user-provided context to generate "
                        "specific and actionable suggestions. Adhere strictly to these guidelines:\n"
                        "- Focus on students and academic success.\n"
                        "- Be empathetic, understanding, and professional.\n"
                        "- Ensure responses are simple and easy to understand, avoiding technical jargon unless necessary.\n"
                        "- Prioritize halal and ethical practices in any recommendations.\n"
                        "- Avoid speculative or unnecessary discussions.\n"
                        "Your goal is to act as a dedicated and helpful academic companion."
                    )
                )
                chat = model.start_chat(history=st.session_state.chat_history)

                # Send user message to chatbot
                response = chat.send_message(user_message)

                # Add the new user and assistant messages to chat history
                st.session_state.chat_history.append({"role": "user", "parts": user_message})
                st.session_state.chat_history.append({"role": "model", "parts": response.text})

            except Exception as e:
                st.error(f"Error: {str(e)}")

        for chat in st.session_state.chat_history:
            role = "You" if chat["role"] == "user" else "AURA"
            st.write(f"**{role}:** {chat['parts']}")
            ## text_to_speech(response.text)

def tell_date():
     # Tells Aura what's the date
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime("%A, %d %B %Y")
    formatted_time = current_datetime.strftime("%I:%M %p")
    st.session_state.chat_history.append({"role": "model", "parts": f"Today's date is {formatted_date}. The time is {formatted_time}"})