'''

Flask app to control a fish feeder

'''

from datetime import datetime
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
templateData = {
	'status' : "Initialising",
	'last_feed' : "Never"
}

@app.route("/")
def main():
	# todo get status from db
	return render_template('main.html', **templateData)

# Only one action possible at the moment, "feed"
@app.route("/<action>")
def action(action):
	if action == "feed":

		conn = sqlite3.connect('/home/pi/turt-mon/turtles.db')
		c = conn.cursor()
		c.execute("UPDATE control SET feedNow=?", [True])
		conn.commit()

		# todo read this from db
		templateData['last_feed'] = str(datetime.now())

	# should this be return redirect?
	return render_template('main.html', **templateData)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)
