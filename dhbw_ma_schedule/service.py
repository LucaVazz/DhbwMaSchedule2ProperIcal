from datetime import timedelta, datetime

from dhbw_ma_schedule.schedule_week import ScheduleWeek
from dhbw_ma_schedule.connector import Connector
from ical_utils import Event, convert_events_to_ical


def fetch_events(uid: str) -> [Event]:
    connection = Connector(uid)
    current_week_schedule = ScheduleWeek(connection.fetch())

    course_name = current_week_schedule.extract_course_name()
    if course_name == '':
        raise FileNotFoundError('A Schedule with the given UID does not exist!')
        # The website just returns an empty schedule-skeleton if the uid is unknown, so we have to catch that

    events = current_week_schedule.extract_events()

    last_schedule = current_week_schedule
    for _ in range(2):
        previous_week_param = last_schedule.extract_previous_week_param()
        schedule = ScheduleWeek(connection.fetch(previous_week_param))
        events += schedule.extract_events()
        last_schedule = schedule

    last_schedule = current_week_schedule
    for _ in range(17):  # approximately 4 months  (30*4/7=17,1429)
        next_week_param = last_schedule.extract_next_week_param()
        schedule = ScheduleWeek(connection.fetch(next_week_param))
        events += schedule.extract_events()
        last_schedule = schedule

    return events

def add_alarms_for_first_day_event(events: [Event], time: str) -> None:
    """
    Adds an alarm offset to each event, which is the first on its respective date.
    :param events: A list of events. The events need to be grouped by date and sorted by their start time. Will be modified.
    :param time: A string like 1900 where the first two chars represent the hour and the last two chars represent the
        minute at which the alarm should be set.
    """
    time_hour = int(time[0:2])
    time_minutes = int(time[2:4])

    for i in range(len(events)):
        if i == 0 or events[i].start.date() != events[i - 1].start.date():
            alarm_date = events[i].start.date() - timedelta(days=1)  # the alarm should ring on the day before the event
            alarm_datetime = datetime(alarm_date.year, alarm_date.month, alarm_date.day, time_hour, time_minutes)
            alarm_total_offset = int((events[i].start - alarm_datetime).total_seconds() / 60)  # offset is in minutes
            #                                                           ^ the timedelta is otherwise split between
            #                                                              full days and remaining seconds
            events[i].alarm_minute_offsets.append(alarm_total_offset)

def add_alarms_before_start(events: [Event], offset: int) -> None:
    for event in events:
        event.alarm_minute_offsets.append(offset)

def generate_ical(events: [Event]) -> str:
    return convert_events_to_ical(events)
