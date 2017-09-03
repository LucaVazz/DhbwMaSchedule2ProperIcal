import datetime


class Event:
    def __init__(self,
        title: str, start: datetime.datetime, end: datetime.datetime, location: str = None, comment: str = None
     ):
        self.title = title
        self.start = start
        self.end = end
        self.location = location
        self.comment = comment


def convert_events_to_ical(events: [Event]) -> str:
    result_str = """BEGIN:VCALENDAR
VERSION:2.0
METHOD:PUBLISH
"""

    result_str += """BEGIN:VTIMEZONE
TZID:Mannheim
BEGIN:STANDARD
DTSTART:19961027T0300
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

    for event in events:
        result_str +=\
            'BEGIN:VEVENT\n' +\
            'SUMMARY:%s\n'%(event.title) +\
            _convert_date_to_ical_kv('DTSTART', event.start) +\
            _convert_date_to_ical_kv('DTEND', event.end) +\
            ('LOCATION:%s\n'%(event.location) if event.location is not None and event.location != '' else '') +\
            ('DESCRIPTION::%s\n'%(event.comment) if event.comment is not None and event.comment != '' else '') +\
            'END:VEVENT\n'

    return result_str + 'END:VCALENDAR\n'

def _convert_date_to_ical_kv(key: str, date: datetime.datetime):
    return '%s;TZID=Mannheim:%s\n'%(key, date.strftime('%Y%m%dT%H%M00'))
