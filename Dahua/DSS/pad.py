import requests
from requests.auth import HTTPDigestAuth

find_access_user_face_token_path = '/cgi-bin/FaceInfoManager.cgi?action=startFind'
find_access_user_face_path = '/cgi-bin/FaceInfoManager.cgi?action=doFind&Token=0&Offset=0&Count=20'
find_multiple_access_user_path = '/cgi-bin/AccessUser.cgi?action=startFind'
find_multiple_access_user_fingerprint_path = '/cgi-bin/AccessFingerprint.cgi?action=get&UserID=1'
add_access_user_path = '/cgi-bin/AccessUser.cgi?action=insertMulti'
add_access_user_face_path = '/cgi-bin/FaceInfoManager.cgi?action=add'
modeify_access_user_path = '/cgi-bin/AccessUser.cgi?action=updateMulti'

event_upload_path = '/cgi-bin/configManager.cgi?action=getConfig&name=PictureHttpUpload'

class Dahua:

	def  __init__(self, hostAddress, username, password):

		self.hostAddress = hostAddress
		self.username = username
		self.password = password

	def find_access_user_face_token(self):

		api_url = self.hostAddress + find_access_user_face_token_path

		response = requests.get( url=api_url, auth=HTTPDigestAuth(self.username, self.password) )


		return response.text

	def find_access_user_face(self):

		api_url = self.hostAddress + find_access_user_face_path

		response = requests.get( url=api_url, auth=HTTPDigestAuth(self.username, self.password) )


		return response.text

	def find_access_user(self):

		api_url = self.hostAddress + find_multiple_access_user_path

		response = requests.get( url=api_url, auth=HTTPDigestAuth(self.username, self.password) )


		return response.text

	def find_access_user_fingerprint(self):

		api_url = self.hostAddress + find_multiple_access_user_fingerprint_path 

		response = requests.get( url=api_url, auth=HTTPDigestAuth(self.username, self.password) )


		return response.text

	def add_user(self):

		api_url = self.hostAddress + add_access_user_path

		requestBody = {
			'UserList' : [

				{
					'UserID' : '2',
					'UserName' : 'test',
					'UserType' : 0
				}

			]
		}

		response = requests.post( url=api_url, json=requestBody, auth=HTTPDigestAuth(self.username, self.password) )

		return response.text

	def add_user_face(self):

		api_url = self.hostAddress + add_access_user_face_path

		requestBody = {
					'UserID' : '2',
					'Info' : {
						"UserName": "ZhangSan"
					}
				}

		

		response = requests.post( url=api_url, json=requestBody, auth=HTTPDigestAuth(self.username, self.password) )

		return response.text

	def modify_user(self):

		api_url = self.hostAddress + add_access_user_face_path

		requestBody = {
					'UserID' : '2',
					'Info' : {
						"UserName": "ZhangSan"
					}
				}

		

		response = requests.post( url=api_url, json=requestBody, auth=HTTPDigestAuth(self.username, self.password) )

		return response.text


	def config_event_upload(self):

		api_url = self.hostAddress + event_upload_path

		response = requests.get( url=api_url, auth=HTTPDigestAuth(self.username, self.password) )

		print(response.text)


if __name__ == '__main__':
	
	pad = Dahua(hostAddress='http://192.168.33.98', username='admin', password='nVk12345')

	# print((pad.add_user()))

	print(pad.find_access_user_fingerprint())

	# print(pad.find_access_user_face_token())
	# print(pad.find_access_user_face())
	# print(pad.find_access_user())
	# print(pad.config_event_upload())
