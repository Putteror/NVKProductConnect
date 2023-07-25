import requests
import hashlib

import time


AUTH_URL = '/brms/api/v1.0/accounts/authorize'
KEEP_ALIVE_URL = '/brms/api/v1.0/accounts/keepalive'
UPDATE_TOKEN_URL = '/brms/api/v1.0/accounts/updateToken'
LOGOUT_URL = '/brms/api/v1.0/accounts/unauthorize'

MQ_CONGIF_URL = '/brms/api/v1.0/BRM/Config/GetMqConfig'
GET_TIME_TEMPLATE_URL = '/brms/api/v1.1/time-template/list'
GET_DEVICE_LIST = '/brms/api/v1.1/device/page'

DOOR_GROUP_PATH = '/obms/api/v1.0/accessControl/doorGroup'
GET_DOOR_GROUP_PATH = '/obms/api/v1.0/accessControl/door-group/page'
DELETE_DOOR_GROUP_PATH = '/obms/api/v1.0/accessControl/doorGroupList'

ACCESS_PERMISSION_GROUP_PATH = '/obms/api/v1.1/acs/access-group'
GET_ACCESS_PERMISSION_GROUP_PATH = '/obms/api/v1.1/acs/access-group/list'
DELETE_ACCESS_PERMISSION_GROUP_PATH = '/obms/api/v1.1/acs/access-group/delete/batch'

PERSON_GROUP_PATH = '/obms/api/v1.1/acs/person-group'
GET_PERSON_GROUP_PATH = '/obms/api/v1.1/acs/person-group/list'


def encryption_md5(string_data):

	encrypt_data = hashlib.md5(string_data.encode('utf-8')).hexdigest()

	return encrypt_data

class DSS:

	def __init__(self, ipAddress, username, password):

		self.ipAddress = ipAddress
		self.hostAddress = 'https://' + ipAddress
		self.username = username
		self.password = password
		self.temp = {}
		self.token = ''

	### Authentication ########################

	def get_token(self):

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

		api_url = self.hostAddress + AUTH_URL

		requestsBody = {

			"signature": signature,
			"userName": self.username,
			"randomKey": randomkey,
			"publicKey": publickey,
			"encryptType": encrypt_type,
			"ipAddress": self.ipAddress,
			"clientType": "WIN"
		}

		response = requests.post(url=api_url, json=requestsBody, verify=False)

		self.token = response.json()['token']

		return response.json()

	def keep_alive(self):

		api_url = self.hostAddress + KEEP_ALIVE_URL

		headers = { 'X-Subject-Token' : self.token , "Content-Type": "Application/json"}

		requestsBody = {

			"token": self.token, 
			"duration": 30 
		}

		response = requests.put(url=api_url, headers=headers, json=requestsBody, verify=False)

		return response.json()

	def update_token(self):

		api_url = self.hostAddress + UPDATE_TOKEN_URL

		headers = { 'X-Subject-Token' : self.token , "Content-Type": "Application/json"}

		signature = encryption_md5( self.temp[4] + ":" + self.token )

		requestsBody = {

			"signature" : signature
		}

		response = requests.post(url=api_url, headers=headers, json=requestsBody, verify=False)

		return response.json()

	def logout(self):

		api_url = self.hostAddress + LOGOUT_URL

		headers = { 'X-Subject-Token' : self.token , "Content-Type": "Application/json"}

		requestsBody = {}

		response = requests.post(url=api_url, headers=headers, json=requestsBody, verify=False)

		return response.json()	

	### API DATA ########################	

	def get_mq_configuration(self):

		api_url = self.hostAddress + MQ_CONGIF_URL

		headers = {'X-Subject-Token' : self.token}

		requestsBody = { 

			"clientType": "WINPC_V2", 
			"project": "PSDK", 
			"method": "BRM.Config.GetMqConfig", 
		}

		response = requests.post(url=api_url, headers=headers, json=requestsBody, verify=False)

		return response.json()


	def get_time_template_list(self):

		api_url = self.hostAddress + GET_TIME_TEMPLATE_URL

		headers = {'X-Subject-Token' : self.token}

		response = requests.get(url=api_url, headers=headers, verify=False)

		return_data = response.json()

		return return_data

	def get_device_list(self, page=1, size=100):

		api_url = self.hostAddress + GET_DEVICE_LIST
		headers = {'X-Subject-Token' : self.token}

		query = {
			'page' : page,
			'pageSize' : size
		}

		response = requests.get(url=api_url, headers=headers, params=query, verify=False)

		return_data = response.json()

		return return_data

	#########################################################
	### Access Control ######################################
	#########################################################

	### Door Group #########################################

	def get_door_group_list(self, page=1, size=100):

		api_url = self.hostAddress + GET_DOOR_GROUP_PATH
		headers = {'X-Subject-Token' : self.token}

		query = {
			'page' : page,
			'pagesize' : size
		}

		response = requests.get(url=api_url, headers=headers, params=query, verify=False)

		return_data = response.json()

		return return_data

	def add_door_group(self, name="APIDoorGroup" , requestsBody=None):

		api_url = self.hostAddress + DOOR_GROUP_PATH
		headers = {'X-Subject-Token' : self.token}

		if requestsBody is None :

			requestsBody = { 	

					"doorGroupName": name,
					"channelIds": [ "1000000$7$0$0" ],

				}
		
		response = requests.post(url=api_url, headers=headers, json=requestsBody, verify=False)

		return_data = response.json()

		return return_data

	def update_door_group(self, door_group_id):

		api_url = self.hostAddress + DOOR_GROUP_PATH
		headers = {'X-Subject-Token' : self.token}

		requestsBody = { 	

				"doorGroupName": "124",
				"channelIds": [ "1000000$7$0$0" ],
			}
		
		response = requests.post(url=api_url, headers=headers, json=requestsBody, verify=False)

		return_data = response.json()

		return return_data

	def delete_door_group(self, door_group_id):

		api_url = self.hostAddress + DELETE_DOOR_GROUP_PATH 
		headers = {'X-Subject-Token' : self.token}

		query = {
			"doorGroupIds" : str(door_group_id)
		}

		response = requests.delete(url=api_url, headers=headers, params=query, verify=False)

		return_data = response.json()

		return return_data

	### Access Group #########################################

	def get_access_permission_group(self):

		api_url = self.hostAddress + GET_ACCESS_PERMISSION_GROUP_PATH

		headers = {'X-Subject-Token' : self.token, }

		response = requests.get(url=api_url, headers=headers, verify=False)

		return_data = response.json()

		return return_data

	def add_access_permission_group(self):

		api_url = self.hostAddress + ACCESS_PERMISSION_GROUP_PATH

		headers = {'X-Subject-Token' : self.token, }

		requestsBody = { 

					"accessGroupName": "123", 
					"doorGroupIds": ["3"], 
					# "remark": "beizhu", 
					# "roleIds":["1","2"] 

					}
		
		response = requests.post(url=api_url, headers=headers, json=requestsBody, verify=False)

		return_data = response.json()

		return return_data

	def update_access_permission_group(self, access_permission_group_id):

		api_url = self.hostAddress + ACCESS_PERMISSION_GROUP_PATH + f'/{access_permission_group_id}'

		headers = {'X-Subject-Token' : self.token, }

		requestsBody = { 

					"accessGroupName": "123", 
					"doorGroupIds": ["3"], 
					# "remark": "beizhu", 
					# "roleIds":["1","2"] 

					}
		
		response = requests.put(url=api_url, headers=headers, json=requestsBody, verify=False)

		return_data = response.json()

		return return_data

	def delete_access_permission_group(self, access_permission_group_id):

		api_url = self.hostAddress + DELETE_ACCESS_PERMISSION_GROUP_PATH

		headers = {'X-Subject-Token' : self.token, }

		requestsBody = { 

					"accessGroupName": "123", 
					"doorGroupIds": ["3"], 
					# "remark": "beizhu", 
					# "roleIds":["1","2"] 

					}
		
		response = requests.delete(url=api_url, headers=headers, json=requestsBody, verify=False)

		return_data = response.json()

		return return_data

	### Person Group ##########

	def get_person_group_list(self):

		api_url = self.hostAddress + GET_PERSON_GROUP_PATH

		headers = {'X-Subject-Token' : self.token, }

		response = requests.get(url=api_url, headers=headers, verify=False)

		return_data = response.json()

		return return_data


if __name__ == '__main__':
	
	dss = DSS(ipAddress='192.168.11.250', username='system', password='nVk12345')

	dss.login()
	dss.keep_alive()

	# print(dss.get_mq_configuration())
	# print(dss.get_time_template_list())
	# print(dss.get_device_list())

	### Access Control ###

	print(dss.get_door_group_list())
	# print(dss.add_door_group())

	# print(dss.delete_door_group(3))

	# print(dss.add_access_permission_group())

	dss.update_token()
	dss.logout()