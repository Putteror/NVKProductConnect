#!/usr/bin/python
# -*- coding: utf-8 -*-
import hashlib
import requests
import json
import time
import base64

CHALLENGE_PATH = '/api/auth/login/challenge'
LOGIN_PATH = '/api/auth/login'
LOGOUT_PATH = '/api/auth/logout'

REBOOT_PATH = '/api/devices/reboot'

EXTRACT_IMAGE_PATH = '/api/devices/feature'
THIRD_PARTY_SERVER_PATH = '/api/subscribe/push'
DEVICE_STATUS_PATH = '/api/devices/status'
ACCESS_CONTROL_PARAMETER_PATH = '/api/devices/door'

PERSON_PATH = '/api/persons/item'
PERSON_LIST_PATH = '/api/persons/query'

UPGRADE_PATH = '/api/devices/firmware'

def encrypt_string(hash_string):
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

def convert_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        base64_data = base64.b64encode(image_data)
        return base64_data.decode('utf-8')
	
class Shenxing():

	def __init__(self, hostAddress, username, password):

		self.hostAddress = hostAddress
		self.username = username
		self.password = password
		self.sessionId = ''

	### Authentication ########################################

	def challenge(self):

		api_url = self.hostAddress + CHALLENGE_PATH + f'?username={self.username}'
		response = requests.get(url=api_url)

		return_data = response.json()

		return return_data
	

	def login(self):

		challenge = self.challenge()

		salt = str(challenge["salt"])
		cha = str(challenge["challenge"])
		session = str(challenge["session_id"])

		key = self.password + salt + cha 

		password_encrypt = encrypt_string(key)

		headers = {'Content-Type': 'application/json'}

		requestsBody = {
			"session_id": session,
			"username": self.username,
			"password": password_encrypt
		}

		api_url =  self.hostAddress + LOGIN_PATH
		response = requests.post(url=api_url, json=requestsBody, headers=headers)

		return_data = response.json()

		self.sessionId = return_data['session_id']

		return return_data
		
	def logout(self):

		api_url = self.hostAddress + LOGOUT_PATH
		headers = {"Cookie" : f'sessionID={self.sessionId}'}

		response = requests.get(url=api_url, headers=headers)

		return_data = response.text

		return return_data, self.sessionId

	### Device Management ########################################

	def extract_image(self, image_path=None, image_base64=None):

		api_url = self.hostAddress + EXTRACT_IMAGE_PATH
		headers = {"Cookie" : f'sessionID={self.sessionId}'}

		if image_path is not None :

			image_base64 = convert_image_to_base64(image_path)

		requestsBody = {

			'picture' : str(image_base64)
		}

		response = requests.post(url=api_url, headers=headers, json=requestsBody)
		return_data = response.json()

		return return_data

	def get_device_status(self):

		api_url = self.hostAddress + DEVICE_STATUS_PATH
		headers = {"Cookie" : f'sessionID={self.sessionId}'}

		response = requests.get(url=api_url, headers=headers)
		return_data = response.json()

		return return_data

	def reboot(self):

		api_url = self.hostAddress + REBOOT_PATH
		headers = {"Cookie" : f'sessionID={self.sessionId}'}

		response = requests.get(url=api_url, headers=headers)
		return_data = response.text

		return return_data

	def set_third_party_server(self, url):

		api_url = self.hostAddress + THIRD_PARTY_SERVER_PATH
		headers = {"Cookie" : f'sessionID={self.sessionId}'}

		requestsBody = {

			'server_uri' : url
		}

		response = requests.put(url=api_url, headers=headers, json=requestsBody)
		return_data = response.json()

		return return_data

	def get_third_party_server(self):

		api_url = self.hostAddress + THIRD_PARTY_SERVER_PATH
		headers = {"Cookie" : f'sessionID={self.sessionId}'}

		response = requests.get(url=api_url, headers=headers)
		return_data = response.json()

		return return_data

	def get_access_control_parameter(self):

		api_url = self.hostAddress + ACCESS_CONTROL_PARAMETER_PATH
		headers = {"Cookie" : f'sessionID={self.sessionId}'}

		response = requests.get(url=api_url, headers=headers)
		return_data = response.json()

		return return_data

	def set_access_control_parameter(self, requestsBody=None):

		api_url = self.hostAddress + ACCESS_CONTROL_PARAMETER_PATH
		headers = {"Cookie" : f'sessionID={self.sessionId}'}

		response = requests.post(url=api_url, headers=headers, json=requestsBody)
		return_data = response.json()

		return return_data

	### Person Management ########################################	

	def get_person_list(self, limit=100, offset=0, requestsBody=None):

		api_url = self.hostAddress + PERSON_LIST_PATH
		headers = {"Cookie" : f'sessionID={self.sessionId}'}

		if not requestsBody :

			requestsBody = {

				"limit" : limit,
				"offset" : offset,
				"sort" : "asc"
			}

		response = requests.post(url=api_url, headers=headers, json=requestsBody)
		return_data = response.json()

		return return_data

	def create_person(self, name="API", person_type="staff", requestsBody=None): 

		## if create fail it still create but no picture

		api_url = self.hostAddress + PERSON_PATH
		headers = {"Cookie" : f'sessionID={self.sessionId}'}

		if not requestsBody :

			requestsBody = {
					"recognition_type": person_type,
					"is_admin" : True,
					"person_name" : name,
					"id":"41578150",
					"group_list": ['1'],
					"face_list" : [{
								"idx" : 0,
								"data" : None
								}]
					}	

		response = requests.post(url=api_url, headers=headers, json=requestsBody)
		return_data = response.json()

		return return_data

	def get_person_by_id(self, person_id):

		api_url = self.hostAddress + PERSON_PATH + '/' + person_id
		headers = {"Cookie" : f'sessionID={self.sessionId}'}

		response = requests.get(url=api_url, headers=headers)
		return_data = response.json()

		return return_data

	def delete_person_by_id(self, person_id):

		api_url = self.hostAddress + PERSON_PATH + '/' + person_id
		headers = {"Cookie" : f'sessionID={self.sessionId}'}

		response = requests.delete(url=api_url, headers=headers)
		return_data = response.text

		return return_data

	### Upgrade ##########

	def upgrade_firmware(self):

		api_url = self.hostAddress + UPGRADE_PATH + '/ota'
		headers = {"Cookie" : f'sessionID={self.sessionId}'}

		requestsBody = {
			'ota_uri' : 'https://naruputter.com/upgrade.bin'
		}
		response = requests.post(url=api_url, json=requestsBody, headers=headers)
		print(response.text)

	def check_status_upgrade_firmware(self):

		api_url = self.hostAddress + UPGRADE_PATH + '/status'
		headers = {"Cookie" : f'sessionID={self.sessionId}'}

		requestsBody = {
			'ota_uri' : 'https://naruputter.com/upgrade.bin'
		}
		response = requests.get(url=api_url, json=requestsBody, headers=headers)
		print(response.text)



if __name__ == '__main__':

	shenxing = Shenxing(hostAddress='http://192.168.90.90', username='admin', password='ifs12345')

	print(shenxing.login())
	# print(shenxing.get_person_list())
	# print(shenxing.reboot())
	# print(shenxing.get_device_status())
	# print(shenxing.create_person(name='testupdate'))
	# print(shenxing.extract_image(image_path='C:/Users/putter/Pictures/Capture.PNG'))
	# print(shenxing.get_third_party_server())
	# print(shenxing.set_third_party_server(url='http://192.168.24.11:5000/callback'))
	# print(shenxing.get_person_by_id('6492c1efa09f09187b877496'))
	# print(shenxing.delete_person_by_id('42855817'))

	# print(shenxing.upgrade_firmware())
	# while True :
	# 	print(shenxing.check_status_upgrade_firmware())
	# 	time.sleep(5)

	# print(shenxing.logout())

	shenxing.download_log()

	#64356494d77a506b1f776618
