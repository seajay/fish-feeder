'''

Fish feeding daemon, reads commands from sqlite db written by the the web server

'''
import gpiozero
from datetime import datetime
from time import sleep
import sqlite3

logfile = open("/home/pi/turt-mon/turtles.log", 'a')
logfile.write("Daemon starting: %(time)s\n" % {'time': datetime.now()})

with sqlite3.connect('/home/pi/turt-mon/turtles.db') as conn:
	c = conn.cursor()
	logfile.write("Daemon connected to db\n")

	while True:
		c.execute('''UPDATE control SET heartBeat=?''', [str(datetime.now())])
		c.execute("SELECT feedNow FROM control")
		feedNow = c.fetchone()[0]

		if feedNow:
		# TODO check not currently feeding or fed too recently
			logfile.write("Got feed command at " + str(datetime.now())+"\n")
			c.execute('''UPDATE control SET status=?''', ["Feeding"])
			c.execute('''UPDATE control SET feedNow=?''', [False])
			# Need to commit this now because the next block sleeps
			conn.commit() 

			try:
				motor = gpiozero.LED(21)
				switch = gpiozero.Button(16, pull_up=True)

				motor.on()
				sleep(5)

				while (switch.is_pressed):
					pass # There must be a better way

				motor.off()

				status = "OK"
				logfile.write("Fed ok\n")
			except Exception as inst:
				status = "Fail"
				logfile.write("Exception feeding:" + str(inst)+"\n")
			finally:
				motor.close()
				switch.close()
				c.execute('''UPDATE control SET status=?''', [status])
				c.execute('''INSERT INTO feeds(time, success) values(?, ?)''', [str(datetime.now()), True if status=="OK" else False])


		conn.commit()
		sleep(1)

