from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
import json, time, sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres:9I4ME8ghDvrBorou@35.232.202.135:5432/irrigation'
db = SQLAlchemy(app)
project_id = "sensor-project-297702"
subscription_id = "test_sub"
# Number of seconds the subscriber should listen for messages
timeout = 5.0

def filterPlantBySerial(serial):
	return Plant.query.filter_by(serial=serial).first()

def movePlant(plant):
	plant.update_status()
	db.session.add(plant)
	db.session.commit()

def changeDryness(plant):
	plant.update_dry()
	db.session.add(plant)
	db.session.commit()

class Plant(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	outside = db.Column(db.Boolean, nullable=False)
	serial = db.Column(db.String(50), nullable=False)
	dry = db.Column(db.Boolean, nullable=False )

	def get_id(self):
		return self.id
	def update_state(self):
		self.outside = not self.outside
	def current_state(self):
		return self.outside
	def isDry(self):
		return self.dry
	def update_dry(self):
		self.dry = not self.dry
	def __repr__(self):
		return f"Plant('{self.id}', '{self.outside}', '{self.serial}', ' {self.dry})"

def callback(message):
	#print(f"Received {message}.")
	data = message.data.decode('utf-8')
	dataJ = json.loads(data)
	attr = message.attributes
	plant = filterPlantBySerial(attr['device_id'])
	if plant.dry != bool(dataJ["need_watering"]):
		changeDryness(plant)
	print(data, attr, plant)

NUM_MESSAGES = 10

# Wrap the subscriber in a 'with' block to automatically call close() to
# close the underlying gRPC channel when done.
while True:
	try:
		subscriber = pubsub_v1.SubscriberClient()
		# The `subscription_path` method creates a fully qualified identifier
		# in the form `projects/{project_id}/subscriptions/{subscription_id}`
		subscription_path = subscriber.subscription_path(project_id, subscription_id)
		response = subscriber.pull(
			request={"subscription": subscription_path, "max_messages": NUM_MESSAGES}
		)
		ack_ids = []
		if len(response.received_messages) > 0:
			for received_message in response.received_messages:
				# print(f"Received: {received_message.message.data}.")
				callback(received_message.message)
				ack_ids.append(received_message.ack_id)

			# Acknowledges the received messages so they will not be sent again.
			subscriber.acknowledge(
				request={"subscription": subscription_path, "ack_ids": ack_ids}
			)

		print(
			f"Received and acknowledged {len(response.received_messages)} messages from {subscription_path}."
		)
		subscriber.close()
	except:  # catch *all* exceptions
		e = sys.exc_info()[0]
		print(">Error: %s" % e)
		time.sleep(10)
	time.sleep(5)