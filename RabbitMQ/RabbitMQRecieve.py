import pika, json, sys, os, requests #, daemon
import time

HOST = "172.21.1.17"
QUEUE_USERNAME = "uih_admin"
QUEUE_PASSWORD = "P@ssw0rd2022"

def callback(ch, method, properties, body):
	data = json.loads(body)
	print(data)
	# URL = "https://dev.face48.com/api/v1/insight/alarms-callback"
	# resp = requests.post(URL, json=data, timeout=7)
	
	# print(resp.text)

# need to download backup file before deploy this file...
# with daemon.DaemonContext():
while True:

	credentials = pika.PlainCredentials(QUEUE_USERNAME, QUEUE_PASSWORD)
	
	parameters = pika.ConnectionParameters(host=HOST, port=5672, virtual_host="face48", credentials=credentials, heartbeat=5)
	
	connection = pika.BlockingConnection(parameters)

	channel = connection.channel()
	# channel.basic_qos(prefetch_count=1)
	channel.basic_consume(queue="face_scan_logs", on_message_callback=callback, auto_ack=True)
	print(1)
	channel.start_consuming()	
	print(1)
