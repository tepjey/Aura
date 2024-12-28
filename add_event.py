from datetime import datetime
from auth import authenticate_user

def add_event_to_calendar(summary, description, start_date, end_date, reminder_minutes):
    try:
        # Get the Google Calendar service
        service = authenticate_user()

        # Define the event
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_date.isoformat(),
                'timeZone': 'Asia/Kuala_Lumpur',
            },
            'end': {
                'dateTime': end_date.isoformat(),
                'timeZone': 'Asia/Kuala_Lumpur',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': reminder_minutes},
                    {'method': 'popup', 'minutes': reminder_minutes},
                ],
            },
        }

        # Insert the event
        created_event = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Event created: {created_event.get('htmlLink')}")
    except Exception as e:
        print(f"An error occurred: {e}")
