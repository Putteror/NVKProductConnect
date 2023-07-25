import requests
import hashlib

import time
import urllib3
import base64
from PIL import Image

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


AUTH_URL = '/brms/api/v1.0/accounts/authorize'
KEEP_ALIVE_URL = '/brms/api/v1.0/accounts/keepalive'
UPDATE_TOKEN_URL = '/brms/api/v1.0/accounts/updateToken'
LOGOUT_URL = '/brms/api/v1.0/accounts/unauthorize'

MQ_CONGIF_URL = '/brms/api/v1.0/BRM/Config/GetMqConfig'
GET_TIME_TEMPLATE_URL = '/brms/api/v1.1/time-template/list'
GET_DEVICE_LIST = '/brms/api/v1.1/device/page'

GET_ACCESS_CONTROL_RULE_PATH = '/obms/api/v1.1/acp/passage/rule/exclude/page'

PERSON_GROUP_PATH = '/obms/api/v1.1/acs/person-group'
GET_PERSON_GROUP_PATH = '/obms/api/v1.1/acs/person-group/list'

PERSON_PATH = '/obms/api/v1.1/acs/person'
GET_PERSON_PATH = '/obms/api/v1.1/acs/person/page'


def encryption_md5(string_data):

	encrypt_data = hashlib.md5(string_data.encode('utf-8')).hexdigest()

	return encrypt_data

def image_to_base64(image_path):
    try:
        # Open the image using PIL/Pillow
        img = Image.open(image_path)

        # Convert the image to a bytes-like object
        with open(image_path, 'rb') as f:
            image_bytes = f.read()

        # Encode the bytes-like object to base64
        base64_image = base64.b64encode(image_bytes).decode('utf-8')

        return base64_image

    except Exception as e:
        print(f"Error converting image to base64: {e}")
        return None

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


	### Access Control #########################################

	def get_access_control_rule_list(self):

		api_url = self.hostAddress + GET_ACCESS_CONTROL_RULE_PATH

		headers = {'X-Subject-Token' : self.token, }

		query = {
			'page':'1',
			'pageSize':'10',
			'resourceType':'2',
			'resourceCode':'resourceCode',
			# 'keyword':keyword

		}

		response = requests.post(url=api_url, headers=headers, params=query, verify=False)

		return_data = response.json()

		return return_data


	### Person Group ##########

	def get_person_group_list(self):

		api_url = self.hostAddress + GET_PERSON_GROUP_PATH

		headers = {'X-Subject-Token' : self.token, }

		response = requests.get(url=api_url, headers=headers, verify=False)

		return_data = response.json()

		return return_data

	### Person ##################

	def add_person(self, requestsBody=None, personId="001", image_path=None):

		api_url = self.hostAddress + PERSON_PATH

		headers = {'X-Subject-Token' : self.token, }

		if image_path is not None :

			image_base64 = image_to_base64(image_path)
		else :

			image_base64 = None

		if requestsBody is None :

			requestsBody = {
								"baseInfo": {
							        "personId": "1125",
							        "lastName": "",
							        "firstName": "Jack",
							        "gender": "2",
							        "orgCode": "001",
							        "email": "",
							        "tel": "18012345678",
							        "remark": "",
							        "source": "0",
							        "facePictures": [image_base64]
							        },
								"extensionInfo": {
							        "nickName": "",
							        "address": "",
							        "idType": "0",
							        "idNo": "",
							        "nationalityId": "9999",
							        "birthday": "",
							        "companyName": "",
							        "department": "",
							        "position": ""
							    },
							    "userDefineFields": [],
							    "residentInfo": {
							        "houseHolder": "0",
							        "sipId": "",
							        "vdpUser": "0"
							    },
							    "authenticationInfo": {
							        "combinationPassword": "",
							        "cards": [],
							        "fingerprints": [],
							        "startTime": "1685980800",
							        "endTime": "2001686399"
							    },
							    "accessInfo": {
							        "accessType": "0",
							        "guestUseTimes": "200",
							        "passageRuleIds": []
							    },
							    "faceComparisonInfo": {
							        "enableFaceComparisonGroup": "0",
							        "faceComparisonGroupId": ""
							    },
							    "entranceInfo": {
							        "enableEntranceGroup": "0",
							        "enableParkingSpace": "0",
							        "parkingSpaceNum": "1",
							        # "vehicles": [
							            
							        # ]
							    }
							
						}
		
		response = requests.post(url=api_url, headers=headers, json=requestsBody, verify=False)

		return_data = response.json()

		return return_data

	def update_person(self, people_id, requestsBody=None):

		api_url = self.hostAddress + PERSON_PATH + f'/{people_id}'

		headers = {'X-Subject-Token' : self.token, }

		if requestsBody is None :

			requestsBody = {
								"baseInfo": {
							        "personId": "1122",
							        "lastName": "",
							        "firstName": "Jack",
							        "gender": "2",
							        "orgCode": "001",
							        "email": "",
							        "tel": "18012345678",
							        "remark": "",
							        "source": "0",
							        },
								"extensionInfo": {
							        "nickName": "",
							        "address": "",
							        "idType": "0",
							        "idNo": "",
							        "nationalityId": "9999",
							        "birthday": "",
							        "companyName": "",
							        "department": "",
							        "position": ""
							    },
							    "userDefineFields": [],
							    "residentInfo": {
							        "houseHolder": "0",
							        "sipId": "",
							        "vdpUser": "0"
							    },
							    "authenticationInfo": {
							        "combinationPassword": "",
							        "cards": [],
							        "fingerprints": [],
							        "startTime": "1685980800",
							        "endTime": "2001686399"
							    },
							    "accessInfo": {
							        "accessType": "0",
							        "guestUseTimes": "200",
							        "passageRuleIds": []
							    },
							    "faceComparisonInfo": {
							        "enableFaceComparisonGroup": "0",
							        "faceComparisonGroupId": ""
							    },
							    "entranceInfo": {
							        "enableEntranceGroup": "0",
							        "enableParkingSpace": "0",
							        "parkingSpaceNum": "0",
							        "vehicles": [
							            {
							                "id": "",
							                "plateNo": "A123C",
							                "vehicleColor": "2",
							                "vehicleBrand": "-1",
							                "remark": "",
							                "entranceGroupIds": [],
							                "entranceLongTerm": "1",
							                "entranceStartTime": "-1",
							                "entranceEndTime": "-1"
							            }
							        ]
							    }
							
						}
		
		response = requests.put(url=api_url, headers=headers, json=requestsBody, verify=False)

		return_data = response.json()

		return return_data

	def get_person_list(self):

		api_url = self.hostAddress + GET_PERSON_PATH

		query = {
			"page" : "1",
			"pageSize" : "30",
			"orgCode" : "001",
			"containChild" : "1"
		}

		headers = {'X-Subject-Token' : self.token, }

		response = requests.get(url=api_url, headers=headers, params=query, verify=False)

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

	print(dss.get_access_control_rule_list())

	### Perosn Group ###

	# print(dss.get_person_group_list())

	### Person ###

	
	# print(dss.add_person(image_path='C:/Users/putter/Pictures/000012.jpg'))
	# print(dss.update_person("1121"))
	# print(dss.get_person_list())

	dss.update_token()
	dss.logout()