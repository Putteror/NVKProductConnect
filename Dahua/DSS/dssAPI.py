import requests
import hashlib
import time
import urllib3
import base64
from PIL import Image

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

'''

DSS Version 8.3

1. Add device in DSS Software
2. < Access Control Page > Create Zone and move device to target zone 
3. < Access Control Page > Create Access Rule and Selecte Zone while create
4. < Person and vehicle info > Add Edit remove people , it will sync to device

'''


def encryption_md5(string_data):

	encrypt_data = hashlib.md5(string_data.encode('utf-8')).hexdigest()

	return encrypt_data

def image_to_base64(filePath):

	with open(filePath, 'rb') as f:

		filePath = f.read()

	base64_data = str(base64.b64encode(filePath))
	base64_data = base64_data.replace("b'","")
	base64_data = base64_data.replace("'","")

	return base64_data

class DSS :

	def __init__(self, hostAddress, username, password):

		self.hostAddress = hostAddress
		self.username = username
		self.password = password
		self.temp = {}
		self.token = ''

		# login when call class

		self.login()
		self.keep_alive()

	####################################################
	### Authentication #################################
	####################################################

	def get_token(self):

		AUTH_URL = '/brms/api/v1.0/accounts/authorize'
		api_url = self.hostAddress + AUTH_URL

		requestsBody = {
			"userName": "system", 
			"ipAddress": "", 
			"clientType": "WINPC_V2"
		}

		response = requests.post(api_url, json=requestsBody, verify=False)
		return_data = response.json()

		return return_data

	def login(self):

		token_respones = self.get_token()

		realm = token_respones['realm']
		randomkey = token_respones['randomKey']
		publickey = token_respones['publickey']
		encrypt_type = token_respones['encryptType']

		self.temp[1] = encryption_md5(self.password)
		self.temp[2] = encryption_md5(self.username + self.temp[1])
		self.temp[3] = encryption_md5(self.temp[2])
		self.temp[4] = encryption_md5(self.username + ":" + realm + ":" + self.temp[3])
		signature = encryption_md5(self.temp[4] + ":" + randomkey)

		AUTH_URL = '/brms/api/v1.0/accounts/authorize'
		api_url = self.hostAddress + AUTH_URL

		requestsBody = {

			"signature": signature,
			"userName": self.username,
			"randomKey": randomkey,
			"publicKey": publickey,
			"encryptType": encrypt_type,
			"ipAddress": self.hostAddress.split('//')[1],
			"clientType": "WIN"
		}

		response = requests.post(url=api_url, json=requestsBody, verify=False)

		try:

			self.token = response.json()['token']

		except:

			print(response.text)

		return response.json()

	def keep_alive(self):

		KEEP_ALIVE_URL = '/brms/api/v1.0/accounts/keepalive'
		api_url = self.hostAddress + KEEP_ALIVE_URL

		headers = { 'X-Subject-Token' : self.token , "Content-Type": "Application/json"}

		requestsBody = {

			"token": self.token, 
			"duration": 30 
		}

		response = requests.put(url=api_url, headers=headers, json=requestsBody, verify=False)

		return response.json()

	def update_token(self):

		UPDATE_TOKEN_URL = '/brms/api/v1.0/accounts/updateToken'
		api_url = self.hostAddress + UPDATE_TOKEN_URL

		headers = { 'X-Subject-Token' : self.token , "Content-Type": "Application/json"}

		signature = encryption_md5( self.temp[4] + ":" + self.token )

		requestsBody = {

			"signature" : signature
		}

		response = requests.post(url=api_url, headers=headers, json=requestsBody, verify=False)

		return response.json()

	def logout(self):

		LOGOUT_URL = '/brms/api/v1.0/accounts/unauthorize'
		api_url = self.hostAddress + LOGOUT_URL

		headers = { 'X-Subject-Token' : self.token , "Content-Type": "Application/json"}

		requestsBody = {}

		response = requests.post(url=api_url, headers=headers, json=requestsBody, verify=False)

		return response.json()	


	####################################################
	### Device Management ##############################
	####################################################

	# 6.2.3.1 Device Information

	def get_device_list(self, page=1, pageSize=30): # 6.2.3.3.2 Get the List of Devices in Pages

		get_device_path = "/brms/api/v1.1/device/page"
		get_device_url = self.hostAddress + get_device_path

		headers = { 'X-Subject-Token' : self.token , "Content-Type": "Application/json"}

		query = {

			"page" : page,	
			"pageSize" : pageSize,
			"orderType" : None
		}

		get_device_response = requests.get( url=get_device_url, headers=headers, verify=False, params=query)

		return get_device_response.json()

	def get_device_by_code(self, deviceCode): # 6.2.3.1.1 Get Device Details

		get_device_info_path = f"/brms/api/v1.1/device/{deviceCode}"
		get_device_info_url = self.hostAddress + get_device_info_path

		headers = { 'X-Subject-Token' : self.token , "Content-Type": "Application/json"}

		get_device_info_response = requests.get( url=get_device_info_url, headers=headers, verify=False )

		return get_device_info_response.json()

	####################################################
	### Person Group ###################################
	####################################################

	# 6.2.8.1 Person Group

	def get_person_group_list(self): # 6.2.8.1.1 Add a Person Group

		get_person_group_path = "/obms/api/v1.1/acs/person-group/list"
		get_person_group_url = self.hostAddress + get_person_group_path

		headers = { 'X-Subject-Token' : self.token , "Content-Type": "Application/json"}

		get_person_group_response = requests.get( url=get_person_group_url, headers=headers, verify=False)

		return get_person_group_response.json()


	####################################################
	### Person #########################################
	####################################################

	# 6.2.8.2 Person Information

	def get_person_list(self, page=1, pageSize=30, group_code="001"): # 6.2.8.2.5 Get the List of Persons in Pages

		get_person_path = "/obms/api/v1.1/acs/person/page"
		get_person_url = self.hostAddress + get_person_path

		headers = { 'X-Subject-Token' : self.token , "Content-Type": "Application/json"}

		query = {

			"page" : page,	
			"pageSize" : pageSize,
			"orgCode" : str(group_code)
		}

		get_person_response = requests.get( url=get_person_url, headers=headers, verify=False, params=query)

		return get_person_response.json()


	####################################################
	### History log #################################### 
	####################################################

	# 6.2.8.3 Access Control Record

	def get_record(self, page=1, size=30, start="1000000000", end=int(time.time())): # 6.2.8.3.1 Obtaining Access Control Records by Page

		get_record_path = "/obms/api/v1.1/acs/access/record/fetch/page"
		get_record_url = self.hostAddress + get_record_path

		headers = { 'X-Subject-Token' : self.token , "Content-Type": "Application/json"}

		requestsBody = {

			"page" : page,
			"pageSize" : size,
			"startTime": str(start), 
			"endTime": str(end)
		}

		get_record_response = requests.post( url=get_record_url, headers=headers, json=requestsBody, verify=False )

		return get_record_response.json()

	def get_record_by_id(self, recordId): # 6.2.8.3.2 Obtaining the Details of Access Control Records

		get_record_info_path = f"/obms/api/v1.1/acs/access/record/{recordId}"
		get_record_info_url = self.hostAddress + get_record_info_path

		headers = { 'X-Subject-Token' : self.token , "Content-Type": "Application/json"}

		get_record_info_response = requests.get( url=get_record_info_url, headers=headers, verify=False )

		return get_record_info_response.json()


	####################################################
	### alarm ##########################################
	####################################################

	# 6.2.6 Alarm(Event Center)

	def set_callback(self, url): # 6.2.6.1 Subscribe to Alarms

		set_callback_path = "/brms/api/v1.1/push-data/alarm/subscribe"
		set_callback_url = self.hostAddress + set_callback_path

		headers = { 'X-Subject-Token' : self.token , "Content-Type": "Application/json"}

		requestsBody = {

			"callbackUrl" : url,
			"action" : 1
		}

		set_callback_response = requests.post( url=set_callback_url, headers=headers, json=requestsBody, verify=False )

		return set_callback_response.text



if __name__ == '__main__':
	
	dss = DSS(hostAddress="https://192.168.11.250", username="system", password="nVk12345")

	# print(dss.get_device_list())
	# print(dss.get_device_by_code("1000003"))

	# print(dss.get_person_group_list())

	# print(dss.get_person_list())

	# print(dss.get_record())
	# print(dss.get_record_by_id("204"))
	# print(dss.set_callback(url="http://192.168.33.37:5000/"))

	print(dss.logout())

