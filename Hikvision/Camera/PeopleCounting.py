import requests
import xmltodict
import json

PROTOCOL_CAPABILITY_PATH = '/ISAPI/Security/adminAccesses/capabilities'
DEVICE_INFORMATION_PATH = '/ISAPI/System/deviceInfo'

REAL_TIME_PEOPLE_COUNT_PATH = '/ISAPI/ContentMgmt/FlashStorage/remove/channels'
SCHEDULE_PEOPLE_COUNT_PATH = '/ISAPI/Event/schedules/countings'


def convert_xml_to_json(xml_string):

    xml_dict = xmltodict.parse(xml_string)
    json_data = json.dumps(xml_dict, indent=4)

    return json_data


class Camera:

	def __init__(self, hostAddress, username, password):

		self.hostAddress = hostAddress
		self.username = username
		self.password = password
		self.auth = requests.auth.HTTPDigestAuth(username, password)

	def get_device_protocal_capability(self):

		api_url = self.hostAddress + PROTOCOL_CAPABILITY_PATH
		response = requests.get(url=api_url, auth=self.auth)

		response_json = convert_xml_to_json(response.text)

		return response_json

	def get_device_information(self):

		api_url = self.hostAddress + DEVICE_INFORMATION_PATH
		response = requests.get(url=api_url, auth=self.auth)

		response_json = convert_xml_to_json(response.text)

		return response_json

	def real_time_people_counting(self):

		api_url = self.hostAddress + REAL_TIME_PEOPLE_COUNT_PATH 
		query = {
			'channelID'  : 1
		}
		response = requests.put(url=api_url, params=query, auth=self.auth)

		response_json = convert_xml_to_json(response.text)

		return response_json

	def get_schedule_of_people_counting(self):

		api_url = self.hostAddress + SCHEDULE_PEOPLE_COUNT_PATH
		response = requests.get(url=api_url, auth=self.auth)

		response_json = convert_xml_to_json(response.text)

		return response_json

if __name__ == '__main__':
	
	camera = Camera(hostAddress='http://192.168.26.137', username='admin', password='nVk12345')
	# print(camera.get_device_protocal_capability())
	# print(camera.get_device_information())
	# print(camera.real_time_people_counting())
	print(camera.get_schedule_of_people_counting())



