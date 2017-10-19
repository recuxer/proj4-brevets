"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config
import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    
    #new timezone and brevet distance variables
    timezone = request.args.get('tz', type=str) 
    b_distance = request.args.get('brev_dist', type=int)
    
    #creates beginning date time arrow object from passed arguments in ajax script
    begintime = arrow.get(request.args.get('bd', type=str) + " " + request.args.get('bt', type=str), 'YYYY-MM-DD HH:mm').replace(tzinfo=timezone).isoformat()
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    open_time = acp_times.open_time(km, b_distance, begintime)
    close_time = acp_times.close_time(km, b_distance, begintime)
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)

#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
