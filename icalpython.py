import json
import uuid
from icalendar import Calendar, Event
from datetime import datetime, time, timedelta, timezone
from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
# from gcsa.recurrence import Recurrence, Frequency
time_zone = """
    BEGIN:VTIMEZONE
    TZID:Asia/Kolkata
    X-LIC-LOCATION:Asia/Kolkata
    BEGIN:STANDARD
    TZOFFSETFROM:+0530
    TZOFFSETTO:+0530
    TZNAME:IST
    DTSTART:19700101T000000
    END:STANDARD
    END:VTIMEZONE
    """
def get_date_from_day(day_str):
    days = {
        "Monday": 1, 
        "Tuesday": 2, 
        "Wednesday": 3, 
        "Thursday": 4, 
        "Friday": 5
    }
    return days.get(day_str, 1)
events=[]
def upload_to_google_calendar(events):
    calendar = GoogleCalendar('c_f1f0d97a18f817ebfe0e957ba2abf7f887e114a1f246aabac4a8a3bd34be4b2f@group.calendar.google.com')
    for event in events:
        calendar.add_event(event)
days=["MO","TU","WE","TH","FR"]
def format_datetime(dt):
    dt_utc = dt.astimezone(timezone.utc)
    return dt_utc
def convert_to_ics(json_file):
    

    cal = Calendar()
    cal.add('prodid', '-//Google Inc//Google Calendar 70.9054//EN')  # Set PRODID
    cal.add('version', '2.0')
    start_date = datetime(2024, 1, 8,tzinfo=timezone(timedelta(hours=5, minutes=30)))
    end_date = datetime(2024, 5, 31,tzinfo=timezone(timedelta(hours=5, minutes=30)))

    current_date = start_date
    i=1
    while current_date <= end_date:
        day_str = current_date.strftime('%A')
        
        for cls in data.get(day_str, []):
            event_time = time(*map(int, cls['time'].split(':')))
            event_date = datetime(current_date.year, current_date.month, current_date.day, event_time.hour, event_time.minute, event_time.second)
            new_uid = str(uuid.uuid4()) + '@google.com'
            event = Event()
            event.add('summary', cls['class'])
            event.add('dtstart', format_datetime(event_date))
            if cls['class'].endswith(" P"):
                event.add('dtend', format_datetime(event_date+timedelta(minutes=100)))
                end_time = (event_date + timedelta(minutes=100)).time()
            else:
                event.add('dtend', format_datetime(event_date+timedelta(minutes=50)))
                end_time = (event_date + timedelta(minutes=50)).time()
            event.add('location', cls['venue'])
            event.add('rrule', {'freq': 'weekly','wkst':'su', 'until': end_date, 'byday': days[i-1]})
            event.add('uid', new_uid)
            recurrence_rule = f'RRULE:FREQ=WEEKLY;UNTIL={end_date.strftime("%Y%m%dT%H%M%SZ")};BYDAY={days[i-1]}'

            event = Event(
                summary=cls['class'],
                start=event_date,
                end=datetime.combine(current_date.date(), end_time),
                recurrence=recurrence_rule,
                uid=new_uid,
                timezone='Asia/Kolkata'
            )
            events.append(event)

        if i==5:
            break
        else:
            current_date += timedelta(days=1)
            i=i+1

    content = cal.to_ical().decode('utf-8')
    content = content.replace('END:VCALENDAR', time_zone + 'END:VCALENDAR')

    return event
    

if __name__ == "__main__":
    with open('2 CO 14.json', 'r') as f:
        data = json.load(f)
    cal=convert_to_ics(data)
    upload_to_google_calendar(cal)
    with open('schedule.ics', 'wb') as f:
        f.write(cal.to_ical())
