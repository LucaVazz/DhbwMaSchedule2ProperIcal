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


def convert_events_to_ical(events: [Event], addTzid: bool = True) -> str:
    result_str = """BEGIN:VCALENDAR
VERSION:2.0
METHOD:PUBLISH
PRODID:-//LUCAVAZZANO.EU//DhbwMaSchedule2ProperIcal//DE
"""

    if addTzid:
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
                'ACTION:DISPLAY\n' +\
                'DESCRIPTION:%s\n'%(event.title) +\
                'END:VALARM\n'

        result_str +=\
            'BEGIN:VEVENT\n' +\
            'UID:%s@dms2pi.%s\n'%(number, socket.getfqdn()) +\
            'SUMMARY:%s\n'%(event.title) +\
            _convert_date_to_ical_kv('DTSTART', event.start, addTzid) +\
            _convert_date_to_ical_kv('DTEND', event.end, addTzid) +\
            _convert_date_to_ical_kv('DTSTAMP', datetime.datetime.now(), addTzid) +\
            ('LOCATION:%s\n'%(event.location) if event.location is not None and event.location != '' else '') +\
            ('DESCRIPTION::%s\n'%(event.comment) if event.comment is not None and event.comment != '' else '') +\
            alarms_str +\
            'END:VEVENT\n'
        number += 1

    return result_str + 'END:VCALENDAR\n'

def _convert_date_to_ical_kv(key: str, date: datetime.datetime, addTzid: bool = True):
    return '%s%s:%s\n'%(
        key,
        (';TZID=Mannheim' if addTzid else ''),
        date.strftime('%Y%m%dT%H%M00')
    )
