import json
import uuid
from datetime import datetime, timedelta, timezone

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

def convert_to_ics(json_file):
    events = []
    start_date = datetime(2024, 1, 8, tzinfo=timezone(timedelta(hours=5, minutes=30)))
    end_date = datetime(2024, 5, 31, tzinfo=timezone(timedelta(hours=5, minutes=30)))

    current_date = start_date
    i = 1

    while current_date <= end_date:
        day_str = current_date.strftime('%A')

        for cls in json_file.get(day_str, []):
            event_time = datetime.strptime(cls['time'], '%H:%M:%S').time()
            event_date = datetime(current_date.year, current_date.month, current_date.day, event_time.hour, event_time.minute, event_time.second)
            new_uid = str(uuid.uuid4()) + '@google.com'

            event = (
                f"BEGIN:VEVENT\n"
                f"SUMMARY:{cls['class']}\n"
                f"DTSTART;TZID=Asia/Kolkata:{event_date.strftime('%Y%m%dT%H%M%S')}\n"
            )

            if cls['class'].endswith(" P"):
                end_time = (event_date + timedelta(minutes=100)).time()
                event += f"DTEND;TZID=Asia/Kolkata:{(event_date + timedelta(minutes=100)).strftime('%Y%m%dT%H%M%S')}\n"
            else:
                end_time = (event_date + timedelta(minutes=50)).time()
                event += f"DTEND;TZID=Asia/Kolkata:{(event_date + timedelta(minutes=50)).strftime('%Y%m%dT%H%M%S')}\n"

            event += (
                f"LOCATION:{cls['venue']}\n"
                f"RRULE:FREQ=WEEKLY;UNTIL={end_date.strftime('%Y%m%dT%H%M%S')};BYDAY={current_date.strftime('%A')[:2]}\n"
                f"UID:{new_uid}\n"
                f"END:VEVENT\n"
            )
            events.append(event)

        if i == 5:
            break
        else:
            current_date += timedelta(days=1)
            i += 1

    ics_content = f"BEGIN:VCALENDAR\n" \
                  f"PRODID:-//Google Inc//Google Calendar 70.9054//EN\n" \
                  f"VERSION:2.0\n"
    
    ics_content += '\n'.join(events)
    ics_content += f"{time_zone}\nEND:VCALENDAR\n"

    return ics_content

if __name__ == "__main__":
    with open('2 CS 7 output.json', 'r') as f:
        data = json.load(f)

    ics_content = convert_to_ics(data)

    with open('2 CS 7 output.ics', 'w') as f:
        f.write(ics_content)
