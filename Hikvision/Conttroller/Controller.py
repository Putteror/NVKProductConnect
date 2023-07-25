import requests
import xmltodict
import json

DEVICE_SYSTEM_CAPABILITY_PATH = '/ISAPI/System/capabilities'
DEVICE_INFORMATION_PATH = '/ISAPI/System/deviceInfo'

CONFIG_CAPABILITY_PATH = '/ISAPI/AccessControl/AcsCfg/capabilities?format=json'
WORKING_STATUS_PATH = '/ISAPI/AccessControl/AcsWorkStatus?format=json'

CARD_CAPBILITY_PATH = '/ISAPI/AccessControl/CardInfo/capabilities?format=json'

def convert_xml_to_json(xml_string):

    xml_dict = xmltodict.parse(xml_string)
    json_data = json.dumps(xml_dict, indent=4)

    return json_data


class AccessController:

	def __init__(self, hostAddress, username, password):

		self.hostAddress = hostAddress
		self.username = username
		self.password = password
		self.auth = requests.auth.HTTPDigestAuth(username, password)


	def get_device_capability(self):

		api_url = self.hostAddress + DEVICE_SYSTEM_CAPABILITY_PATH
		response = requests.get(url=api_url, auth=self.auth)

		response_json = convert_xml_to_json(response.text)

		return response_json


	def get_device_information(self):

		api_url = self.hostAddress + DEVICE_INFORMATION_PATH
		response = requests.get(url=api_url, auth=self.auth)

		response_json = convert_xml_to_json(response.text)

		return response_json

	### Access Cotrol General

	def get_config_capability(self):

		api_url = self.hostAddress + CONFIG_CAPABILITY_PATH
		response = requests.get(url=api_url, auth=self.auth)

		response_json = response.json()

		return response_json

	def get_working_status(self):

		api_url = self.hostAddress + WORKING_STATUS_PATH
		response = requests.get(url=api_url, auth=self.auth)

		response_json = response.json()

		return response_json

	### Person and Credential ###

	def get_card_capability(self):

		api_url = self.hostAddress + CARD_CAPBILITY_PATH
		response = requests.get(url=api_url, auth=self.auth)

		response_json = response.json()

		return response_json



if __name__ == '__main__':
	
	controller = AccessController(hostAddress='http://192.168.26.40', username='admin', password='nVk12345')
	# print(controller.get_device_capability())
	# print(controller.get_device_information())
	# print(controller.get_config_capability())
	# print(controller.get_working_status())

	print(controller.get_card_capability())



