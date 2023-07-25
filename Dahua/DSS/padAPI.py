import requests
from requests.auth import HTTPDigestAuth
import base64


def image_to_base64(filePath):

	with open(filePath, 'rb') as f:

		filePath = f.read()

	base64_data = str(base64.b64encode(filePath))
	base64_data = base64_data.replace("b'","")
	base64_data = base64_data.replace("'","")

	return base64_data



class Dahua :

	def  __init__(self, hostAddress, username, password):

		self.hostAddress = hostAddress
		self.username = username
		self.password = password

	### People ###########################################

	def get_all_person(self, offset=0, count=30): #12.4.6, 12.4.7

		request_token_path = "/cgi-bin/AccessUser.cgi?action=startFind"
		request_token_api_url = self.hostAddress + request_token_path

		request_token_response = requests.get( url=request_token_api_url, auth=HTTPDigestAuth(self.username, self.password) )

		try:

			token_json = request_token_response.json()

		except:

			return request_token_response.text


		get_all_person_path = "/cgi-bin/AccessUser.cgi?action=doFind"
		get_all_person_api_url = self.hostAddress + get_all_person_path

		query = {

			'Token' : token_json['Token'],
			'Offset' : offset,
			'Count' : count

		}

		get_all_person_response = requests.get( url=get_all_person_api_url, auth=HTTPDigestAuth(self.username, self.password) , params=query)

		try:

			return_data = get_all_person_response.json()

		except:

			return_data = get_all_person_response.text

		return return_data

	def create_person(self, personId, name): # 12.4.1 

		### if id was existed . it will update 

		create_person_path = "/cgi-bin/AccessUser.cgi?action=insertMulti"
		create_person_url = self.hostAddress + create_person_path

		requestsBody = {

						"UserList" : [
							{
								"UserID" : personId,
								"UserName" : name
							}
						]
					}

		create_person_response = requests.post( url=create_person_url, auth=HTTPDigestAuth(self.username, self.password) , json=requestsBody)

		return create_person_response.text


	def update_person_image(self, personId, imagePath): # 12.4.23

		update_person_image_path = "/cgi-bin/AccessFace.cgi?action=updateMulti"
		update_person_image_url = self.hostAddress + update_person_image_path

		requestsBody = { 
			"FaceList":
				[ 
					{ 
						"UserID": personId, 
						"PhotoData": [ image_to_base64(imagePath) ], 
				}
			] 
		}

		update_person_image_response = requests.post( url=update_person_image_url, auth=HTTPDigestAuth(self.username, self.password), json=requestsBody )

		return update_person_image_response.text


	def get_person_image(self, personIds):

		get_person_image_path = "/cgi-bin/AccessFace.cgi?action=list"
		get_person_image_url = self.hostAddress + get_person_image_path

		query = {}

		if type(personIds) == list :

			for i in range(len(personIds)):

				query[f'UserIDList[{i}]'] = personIds[i]

		else:

			query['UserIDList[0]'] = personIds


		get_person_image_response = requests.get( url=get_person_image_url, auth=HTTPDigestAuth(self.username, self.password), params=query )

		return get_person_image_response.text

	### Log ###################################

	def get_log(self):

		query =  {
		    "action": "findFile",
		    "object": "1791314040",
		    "condition.Channel": "1",
		    "condition.StartTime": "2023-07-21 11:00:00",
		    "condition.EndTime": "2023-07-24 12:00:00"
		}

		# get_log_path = '/cgi-bin/log.cgi?action=startFind&condition.StartTime=2022-7-23 12:00:00&condition.EndTime=2022-7-25 12:00:00'

		# get_log_path = '/cgi-bin/mediaFileFind.cgi?action=factory.create'
		# get_log_path = "/cgi-bin/mediaFileFind.cgi?action=findFile&object=1791314040&condition.Channel=1&condition.StartTime=2022-01-01 11:00:00&condition.EndTime=2022-07-24 12:00:00"
		get_log_path = "/cgi-bin/mediaFileFind.cgi"
		# get_log_path = '/cgi-bin/mediaFileFind.cgi?action=findNextFile&object=1791314040&count=100'
		get_log_url = self.hostAddress + get_log_path

		get_log_response = requests.get(url=get_log_url, auth=HTTPDigestAuth(self.username, self.password), params=query)

		return get_log_response.text


	### callback ###############################

	def callback(self):

		config_callback_path = "/cgi-bin/configManager.cgi?action=getConfig&name=EventHttpUpload"
		config_callback_url = self.hostAddress + config_callback_path

		# query = {

		# 	"ReportHttpUpload" : {
		# 		"ReportHttpUpload" : {
		# 			"Enable" : True,

		# 		},
		# 		"UploadServerList" : {
		# 			"Address" : "127.0.0.1"
		# 		}
		# 	}
		# }

		response = requests.post( url=config_callback_url, auth=HTTPDigestAuth(self.username, self.password) )

		print(response.text)


if __name__ == '__main__':
	
	pad = Dahua(hostAddress='http://192.168.33.98', username='admin', password='nVk12345')

	# print(pad.get_all_person())
	# print(pad.create_person("12", "putty"))
	# print(pad.get_person_image(personIds=[1,2]))

	print(pad.get_log())

	# print(pad.create_person_image())


