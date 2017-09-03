import sys
from flask import Flask, abort

from main import fetch_events, generate_ical


app = Flask(__name__)

@app.route('/<uid>/ical.ical')
def serve_ical(uid):
    try:
        events = fetch_events(uid)
    except FileNotFoundError:
        abort(404)
        return

    return generate_ical(events)


if __name__ == '__main__':
    app.run(debug=('pydevd' in sys.modules))
    #               ^ present if i.e. PyCharm Debugger is attached
