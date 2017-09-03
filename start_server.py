import sys

import flask
from flask import Flask, abort

from main import fetch_events, generate_ical


app = Flask(__name__)

@app.route('/<uid>/ical.ics')
def serve_ical(uid):
    try:
        events = fetch_events(uid)
    except FileNotFoundError:
        app.logger.error('uid %s not found!'%(uid))
        abort(404)
        return

    ical_str = generate_ical(events)
    res = flask.make_response(ical_str)

    res.headers.set('Content-Disposition', 'attachment; filename="ical.ics"')
    res.headers.set('Filename', 'ical.ics')
    res.headers.set('Content-Type', 'text/Calendar')

    app.logger.info('Delivering iCal for uid %s.'%(uid))
    return res


if __name__ == '__main__':
    app.run(debug=('pydevd' in sys.modules))
    #               ^ present if i.e. PyCharm Debugger is attached
