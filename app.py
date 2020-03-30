'''

Flask app to control a fish feeder

'''

import gpiozero
from time import sleep
from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)
templateData = {
	'last_feed' : "Never"
}

@app.route("/")
def main():

	return render_template('main.html', **templateData)

# Only one action possible at the moment, "feed"
@app.route("/<action>")
def action(action):
	if action == "feed":
		motor = gpiozero.LED(21)
		switch = gpiozero.Button(16, pull_up=True)

		motor.on()
		sleep(5)

		while (switch.is_pressed):
        		pass

		motor.off()
		templateData['last_feed'] = str(datetime.now())
	return render_template('main.html', **templateData)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)
