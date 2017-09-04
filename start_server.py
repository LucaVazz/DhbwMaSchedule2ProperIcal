import sys

import flask
from flask import Flask, abort, request

from main import fetch_events, generate_ical, add_alarms_for_first_day_event, add_alarms_before_start

app = Flask(__name__)

@app.route('/<uid>')
def serve_ical(uid):
    try:
        events = fetch_events(uid)
    except FileNotFoundError:
        app.logger.error('uid %s not found!'%(uid))
        abort(404)
        return

    alarmtimeAtDayBefore = request.args.get('alarmtimeAtDayBefore')
    if alarmtimeAtDayBefore is not None:
        add_alarms_for_first_day_event(events, alarmtimeAtDayBefore)

    alarmOffsetBeforeStart = request.args.get('alarmOffsetBeforeStart')
    if alarmOffsetBeforeStart is not None:
        add_alarms_before_start(events, int(alarmOffsetBeforeStart))

    doNotAddTz = request.args.get('doNotAddTz')
    if alarmOffsetBeforeStart is None:
        addTz = False
    else:
        addTz = True

    ical_str = generate_ical(events, addTz)
    res = flask.make_response(ical_str)

    res.headers.set('Content-Disposition', 'attachment; filename="ical.ics"')
    res.headers.set('Filename', 'ical.ics')
    res.headers.set('Content-Type', 'text/Calendar; charset=UTF-8')

    app.logger.info('Delivering iCal for uid %s.'%(uid))
    return res


if __name__ == '__main__':
    app.run(debug=('pydevd' in sys.modules))
    #               ^ present if i.e. PyCharm Debugger is attached
