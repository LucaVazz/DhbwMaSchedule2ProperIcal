from DhbwMaScheduleWeek import DhbwMaScheduleWeek
from DhbwMaScheduleConnector import DhbwMaScheduleConnector
from Ical import convert_events_to_ical

c = DhbwMaScheduleConnector('6705001')
base_schedule = DhbwMaScheduleWeek(c.fetch())

events = base_schedule.extract_events()

last_schedule = base_schedule
for _ in range(2):
    schedule = DhbwMaScheduleWeek(c.fetch(last_schedule.extract_previous_week_param()))
    events += schedule.extract_events()
    last_schedule = schedule

last_schedule = base_schedule
for _ in range(17):  # approximately 4 months
    schedule = DhbwMaScheduleWeek(c.fetch(last_schedule.extract_next_week_param()))
    events += schedule.extract_events()
    last_schedule = schedule

ical_str = convert_events_to_ical(events)
with open('test.ical', 'w') as f:
    f.write(ical_str)
