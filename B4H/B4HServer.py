import requests
from requests.auth import HTTPDigestAuth

API_PATH = '/v1/MEGBOX'

PUBLIC_PARAMETER_PATH = '/configs'
TRIGGER_RELAY_PATH = '/relayTrigger'


class B4H:

	def __init__(self, hostAddress, username, password):

		self.hostAddress = hostAddress
		self.username = username
		self.password = password
		self.auth = HTTPDigestAuth(self.username, self.password)

	# def setting_public_parameters(self):

	# 	api_url = self.hostAddress + API_PATH + PUBLIC_PARAMETER_PATH

	# 	response = requests.post(url=api_url, auth=self.auth, verify=False)

	# 	print(response.text)

	def get_current_public_parameters(self):

		api_url = self.hostAddress + API_PATH + PUBLIC_PARAMETER_PATH

		response = requests.get(url=api_url, auth=self.auth, verify=False)
		return_data = response.json()

		return return_data

	def trigger_relay(self, video_no):

		api_url = self.hostAddress + API_PATH + TRIGGER_RELAY_PATH + '/' + str(video_no)

		response = requests.post(url=api_url, auth=self.auth, verify=False)
		print(response.text)


if __name__ == '__main__':
	
	b4h_server = B4H(hostAddress='https://192.168.33.148', username='admin', password='P@ssw0rdnvk48')

	# print(b4h_server.get_current_public_parameters())
	b4h_server.trigger_relay(3)

