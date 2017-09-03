from DhbwMaScheduleWeek import DhbwMaScheduleWeek
from DhbwMaScheduleConnector import DhbwMaScheduleConnector
from Ical import Event, convert_events_to_ical


def fetch_events(uid: str) -> [Event]:
    connection = DhbwMaScheduleConnector(uid)
    base_schedule = DhbwMaScheduleWeek(connection.fetch())

    if base_schedule.extract_course_name() == '':
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

def generate_ical(events: [Event]) -> str:
    return convert_events_to_ical(events)
