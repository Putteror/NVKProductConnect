import requests

SUCCESS_CODE = 0

LOGIN_PATH = '/auth/login'
PERSON_PATH = '/subject'
ACCESS_CONTROL_GROUP_PATH = '/devices/screens/group/list'

class Koala :

	def __init__(self, hostAddress, username, password):

		self.hostAddress = hostAddress
		self.username = username
		self.password = password
		self.token = self.login()['data']['auth_token']

	def login(self):

		api_url = self.hostAddress + LOGIN_PATH

		headers = {
			'Content-Type' : 'application/json',
			'user-agent' : 'Koala Admin'
		}

		requestsBody = {

			"username" : self.username,
			"password" : self.password,
			'auth_token' : True

		}

		response = requests.post(url=api_url, headers=headers, json=requestsBody)
		response_json = response.json()

		return response_json

	def get_person_list(self, person_type='employee', query=None):

		api_url = self.hostAddress + PERSON_PATH + "/list"

		headers = {
			# 'Content-Type' : 'application/json',
			'Authorization': self.token
		}


		if query is None :

			query = {
				'category' : person_type
			}

		elif 'category' not in query :

			query['category'] = person_type

		response = requests.get(url=api_url, headers=headers, params=query)

		response_json = response.json()

		return response_json

	def get_person_by_id(self, subject_id):

		api_url = self.hostAddress + PERSON_PATH + f"/{str(subject_id)}"

		headers = {
			# 'Content-Type' : 'application/json',
			'Authorization': self.token
		}


		response = requests.get(url=api_url, headers=headers)

		response_json = response.json()

		return response_json



	def get_access_control_group_list(self, query=None):

		api_url = self.hostAddress + ACCESS_CONTROL_GROUP_PATH

		headers = {
			'Content-Type' : 'application/json',
			'Authorization': self.token
		}

		response = requests.get(url=api_url, headers=headers, params=query)

		response_json = response.json()

		return response_json


if __name__ == '__main__':
	
	# koala = Koala(hostAddress='http://192.168.20.102/', username='tor@nvk.co.th', password='nVk123456')
	koala = Koala(hostAddress='http://172.21.1.16/', username='admin@ddc.mail.go.th', password='admin1234')

	# person_list = koala.get_person_list()
	person_info = koala.get_person_by_id(subject_id=2876)
	# access_control_group_list = koala.get_access_control_group_list()

	# print(access_control_group_list)

	print(person_info)
