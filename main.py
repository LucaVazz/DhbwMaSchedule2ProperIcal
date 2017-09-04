from datetime import timedelta, datetime

from DhbwMaScheduleWeek import DhbwMaScheduleWeek
from DhbwMaScheduleConnector import DhbwMaScheduleConnector
from Ical import Event, convert_events_to_ical


def fetch_events(uid: str) -> [Event]:
    connection = DhbwMaScheduleConnector(uid)
    base_schedule = DhbwMaScheduleWeek(connection.fetch())

    course_name = base_schedule.extract_course_name()
    if course_name == '':
        raise FileNotFoundError('A Schedule with the given UID does not exist!')

    events = base_schedule.extract_events()

    last_schedule = base_schedule
    for _ in range(2):
        schedule = DhbwMaScheduleWeek(connection.fetch(last_schedule.extract_previous_week_param()))
        events += schedule.extract_events()
        last_schedule = schedule

    last_schedule = base_schedule
    for _ in range(17):  # approximately 4 months
        schedule = DhbwMaScheduleWeek(connection.fetch(last_schedule.extract_next_week_param()))
        events += schedule.extract_events()
        last_schedule = schedule

    return events

def add_alarms_for_first_day_event(events: [Event], time: str) -> None:
    """
    Adds a alarm offset to each event, which is the first on its respective date.
    :param events: A list of events. The events need to be grouped by date and sorted by their start time. Will be modified.
    :param time: a string like 1900 where the first two chars represent the hour and the last two chars represent the
        minute at which the alarm should be set.
    """
    time_hour = int(time[0:2])
    time_minutes = int(time[2:4])

    for i in range(len(events)):
        if i == 0 or events[i].start.date() != events[i - 1].start.date():
            alarm_date = events[i].start.date() - timedelta(days=1)
            alarm_datetime = datetime(alarm_date.year, alarm_date.month, alarm_date.day, time_hour, time_minutes)
            events[i].alarm_minute_offsets.append(int((events[i].start - alarm_datetime).total_seconds() / 60))

def add_alarms_before_start(events: [Event], offset: int) -> None:
    for event in events:
        event.alarm_minute_offsets.append(offset)

def generate_ical(events: [Event], addTzid: bool = True) -> str:
    return convert_events_to_ical(events, addTzid)
