import datetime
import socket


class Event:
    def __init__(self,
        title: str, start: datetime.datetime, end: datetime.datetime, location: str = None, comment: str = None
     ):
        self.title = title
        self.start = start
        self.end = end
        self.location = location
        self.comment = comment
        self.alarm_minute_offsets = []


def convert_events_to_ical(events: [Event]) -> str:
    result_str = """BEGIN:VCALENDAR
VERSION:2.0
METHOD:PUBLISH
PRODID:-//LUCAVAZZANO.EU//DhbwMaSchedule2ProperIcal//DE
"""

    result_str += """BEGIN:VTIMEZONE
TZID:Mannheim
BEGIN:STANDARD
DTSTART:19961027T030000Z
RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
TZNAME:GMT+01:00
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19810329T020000Z
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU
TZOFFSETFROM:+0100
TZOFFSETTO:+0200
TZNAME:GMT+02:00
END:DAYLIGHT
END:VTIMEZONE
"""

    number = 0
    for event in events:
        alarms_str = ''
        for offset in event.alarm_minute_offsets:
            alarms_str +=\
                'BEGIN:VALARM\n' +\
                'TRIGGER:-PT%sM\n'%(offset) +\
                'ACTION:AUDIO\n' +\
                'DESCRIPTION:%s\n'%(event.title) +\
                'END:VALARM\n'

        result_str +=\
            'BEGIN:VEVENT\n' +\
            'UID:%s@dms2pi.%s\n'%(number, socket.getfqdn()) +\
            'SUMMARY;CHARSET=UTF-8:%s\n'%(sanitize_for_ical(event.title)) +\
            _convert_date_to_ical_kv('DTSTART', event.start) +\
            _convert_date_to_ical_kv('DTEND', event.end) +\
            _convert_date_to_ical_kv('DTSTAMP', datetime.datetime.now()) +\
            ('LOCATION;CHARSET=UTF-8:%s\n'%(sanitize_for_ical(event.location)) if
                event.location is not None and event.location != '' else '') +\
            ('DESCRIPTION;CHARSET=UTF-8:%s\n'%(sanitize_for_ical(event.comment)) if
                event.comment is not None and event.comment != '' else '') +\
            alarms_str +\
            'END:VEVENT\n'
        number += 1

    return result_str + 'END:VCALENDAR\n'

def _convert_date_to_ical_kv(key: str, dateValue: datetime.datetime):
    return '%s;TZID=Mannheim:%s\n'%(
        key,
        dateValue.strftime('%Y%m%dT%H%M00')
    )

def sanitize_for_ical(text: str) -> str:
    return text.replace('\\', '/').replace('\r\n', '\\n').replace('\n', '\\n')
