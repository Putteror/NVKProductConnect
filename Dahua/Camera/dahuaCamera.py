import requests
from requests.auth import HTTPDigestAuth
import base64
from PIL import Image
from io import BytesIO

def save_jpeg_data_to_file(jpeg_data, filename):
    with open(filename, 'wb') as f:
        f.write(jpeg_data)


class Dahua:

	def  __init__(self, hostAddress, username, password):

		self.hostAddress = hostAddress
		self.username = username
		self.password = password

	def get_network_interfaces(self):

		api_path = "/cgi-bin/netApp.cgi?action=getInterfaces"
		api_url = self.hostAddress + api_path

		query = {}


		get_snapshot_resp = requests.get( url=api_url, auth=HTTPDigestAuth(self.username, self.password) , params=query)


		try:

			return_data = get_snapshot_resp.json()

		except:

			return_data = get_snapshot_resp.text


		return return_data


	def get_snapshot(self):

		api_path = "/cgi-bin/snapshot.cgi"
		api_url = self.hostAddress + api_path

		query = {

			"type" : 0

		}

		get_snapshot_resp = requests.get( url=api_url, auth=HTTPDigestAuth(self.username, self.password) , params=query)

		print(get_snapshot_resp.iter_content())

		try:

			return_data = get_snapshot_resp.json()

		except:

			return_data = get_snapshot_resp.content

			save_jpeg_data_to_file(return_data, "image.jpg")


		return return_data

if __name__ == '__main__':
	
	camera = Dahua( hostAddress="http://192.168.33.108", username="admin", password="nVk12345" )

	(camera.get_snapshot())