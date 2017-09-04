import sys

from flask import Flask, abort, request, make_response

from dhbw_ma_schedule.service import fetch_events, generate_ical, add_alarms_for_first_day_event, add_alarms_before_start


app = Flask(__name__)

@app.route('/<uid>')
def serve_ical(uid):
    try:
        events = fetch_events(uid)
    except FileNotFoundError:
        app.logger.error('Aborting request for uid %s, uid not found!'%(uid))
        abort(404)
        return  # technically not needed, but PyCharm doesn't know that

    alarmtimeAtDayBefore = request.args.get('addAlarmtimeAtDayBefore')
    if alarmtimeAtDayBefore is not None:
        add_alarms_for_first_day_event(events, alarmtimeAtDayBefore)

    alarmOffsetBeforeStart = request.args.get('addAlarmOffsetBeforeStart')
    if alarmOffsetBeforeStart is not None:
        add_alarms_before_start(events, int(alarmOffsetBeforeStart))

    ical_str = generate_ical(events)

    res = make_response(ical_str)
    res.headers.set('Content-Disposition', 'attachment; filename="ical.ics"; charset=utf-8')
    res.headers.set('Filename', 'ical.ics')
    res.headers.set('Content-Type', 'text/Calendar; charset=utf-8')

    app.logger.info('Delivering iCal for uid %s.'%(uid))
    return res


if __name__ == '__main__':
    # Executed if run locally (i.e. not via WSGI):
    app.run(debug=('pydevd' in sys.modules))
    #               ^ present if i.e. PyCharm Debugger is attached
