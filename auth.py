import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import streamlit as st

# Define the scope for accessing the Google Calendar API
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def authenticate_user():
    creds = None
    # Check if token.json exists
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If no valid credentials, prompt login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Use client config directly from Streamlit secrets
            credentials_data = {
                "installed": {
                    "client_id": st.secrets["google_credentials"]["client_id"],
                    "project_id": st.secrets["google_credentials"]["project_id"],
                    "auth_uri": st.secrets["google_credentials"]["auth_uri"],
                    "token_uri": st.secrets["google_credentials"]["token_uri"],
                    "auth_provider_x509_cert_url": st.secrets["google_credentials"]["auth_provider_x509_cert_url"],
                    "client_secret": st.secrets["google_credentials"]["client_secret"],
                    "redirect_uris": [st.secrets["google_credentials"]["redirect_uri"]],
                }
            }

            flow = InstalledAppFlow.from_client_config(credentials_data, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)
