#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LOGIN_URL = '/api/v1/users/authentication'
LOGOUT_URL = '/api/v2/logout'

CALLBACK_URL = '/api/v1/cb/'

ACCESS_CONTROL_GROUP_URL = '/api/v1/access-control-group'
ACCESS_CONTROL_RULE_URL = '/api/v1/access-control-rule'

COMPANY_URL = '/api/v1/company'

EVENT_URL = '/api/v1/events'
EVENT_FORM_URL = '/api/v1/form'

GUARD_TOUR_URL = '/fastapi/v1/guard-tour-schedule'

HISTORY_URL = '/api/v1/history/events/'

PEOPLE_URL = '/api/v1/people'
SEARCH_PEOPLE_URL = '/api/v1/people/search'
EXPORT_PEOPLE_URL = '/api/v1/people/export'

class Face48 :

	def __init__(self, hostAddress, username, password):

		self.hostAddress = hostAddress
		self.username = username
		self.password = password
		self.accessToken = ''

	def login(self):

		api_url = self.hostAddress + LOGIN_URL

		headers = { 'Content-Type' : 'Application/json' }

		requestsBody = {

			'username' : self.username,
			'password' : self.password
		}

		response = requests.post(url=api_url, headers=headers, json=requestsBody, verify=False)
		return_data = response.json()

		self.accessToken = return_data['access_token']

		return return_data

	def logout(self):

		api_url = self.hostAddress + LOGOUT_URL

		headers = { 'Content-Type' : 'Application/json', 'Authorization' : f'Bearer { self.accessToken }'}

		response = requests.post(url=api_url, headers=headers, verify=False)
		return_data = response.json()

		return return_data

	def sudo_face_scan(self, path, requestsBody=None):

		api_url = self.hostAddress + CALLBACK_URL + path

		now_timestamp = int(time.time())*1000

		headers = { 'Content-Type' : 'Application/json' }

		if not requestsBody :

			requestsBody = 	{

				"blur": 0.8,
				"card_number": "",
				"device_ip": "192.168.33.108",
				"device_sn": "M014200662006001144",
				"device_token": "e5d21f69439d40e9b4eea6f249a13994",
				"liveness_score": 99,
				"liveness_type": 1,
				"mask_type": 0,
				"pass_type": 1,
				"person_code": "",
				"person_id": "64384da4ccec99c7197be4f1",
				"person_name": "Putter Test",
				"recognition_score": 85,
				"recognition_type": 2,
				"server_verify": 0,
				"temperature": 0.0,
				"temperature_type": 0,
				"timestamp": now_timestamp,
				"verification_mode": 0,
				"verification_type": 0
			}

		response = requests.post(url=api_url, json=requestsBody, headers=headers)
		return_data = response.text

		return return_data


	##### ACESS CONTROL GROUP ##############

	def get_access_control_group_list(self):

		api_url = self.hostAddress + ACCESS_CONTROL_GROUP_URL

		headers = { 'Content-Type' : 'Application/json', 'Authorization' : f'Bearer { self.accessToken }'}

		response = requests.get(url=api_url, headers=headers)
		return_data = response.json()

		return return_data


	def create_access_control_group(self, name="API", device_type="shenxing", requestsBody=None):

		api_url = self.hostAddress + ACCESS_CONTROL_GROUP_URL

		headers = { 'Content-Type' : 'Application/json', 'Authorization' : f'Bearer { self.accessToken }'}

		if not requestsBody :

			requestsBody = {

				"name": name,
				"_type": device_type,
				"screenIds": []
			}

		response = requests.post(url=api_url, headers=headers, json=requestsBody)
		return_data = response.json()

		return return_data

	def get_access_control_group_by_id(self, group_id):

		api_url = self.hostAddress + ACCESS_CONTROL_GROUP_URL + '/' + str(group_id)

		headers = { 'Content-Type' : 'Application/json', 'Authorization' : f'Bearer { self.accessToken }'}

		response = requests.get(url=api_url, headers=headers)
		return_data = response.json()

		return return_data

	'''

	def update_access_control_group_by_id(self, group_id, name="API Update", device_type="shenxing", requestsBody=None):

		api_url = self.hostAddress + ACCESS_CONTROL_GROUP_URL + '/' + str(group_id)

		headers = { 'Content-Type' : 'Application/json', 'Authorization' : f'Bearer { self.accessToken }'}

		if not requestsBody :

			requestsBody = {

				"name": name,
				"_type": device_type,
				"screenIds": []
			}

		response = requests.post(url=api_url, headers=headers, json=requestsBody)
		return_data = response.json()

		return return_data

	'''

	def delete_access_control_group_by_id(self, group_id):

		api_url = self.hostAddress + ACCESS_CONTROL_GROUP_URL + '/' + str(group_id)

		headers = { 'Content-Type' : 'Application/json', 'Authorization' : f'Bearer { self.accessToken }'}

		response = requests.delete(url=api_url, headers=headers)
		return_data = response.json()

		return return_data

	##### ACESS CONTROL RULE ##############

	def get_access_control_rule_list(self):

		api_url = self.hostAddress + ACCESS_CONTROL_RULE_URL

		headers = { 'Content-Type' : 'Application/json', 'Authorization' : f'Bearer { self.accessToken }'}

		response = requests.get(url=api_url, headers=headers)
		return_data = response.json()

		return return_data

	'''

	def create_access_control_rule(self, name="API", device_type="shenxing", requestsBody=None):

		api_url = self.hostAddress + ACCESS_CONTROL_RULE_URL

		headers = { 'Content-Type' : 'Application/json', 'Authorization' : f'Bearer { self.accessToken }'}

		if not requestsBody :

			requestsBody = {

				"name":name,
				"openAccessScheduleId":"5f47xx4ax9f1e614f3aexxxx",
				"accessControlGroupIds":["5fxx6bx66b56cb48886exxxx"],
				"peopleGroupId":"5x98fxxd8319bxfb964cxxxx"
			}

		response = requests.post(url=api_url, headers=headers, json=requestsBody)
		return_data = response.json()

		return return_data

	'''

	def get_access_control_rule_by_id(self, rule_id):

		api_url = self.hostAddress + ACCESS_CONTROL_RULE_URL + '/' + str(rule_id)

		headers = { 'Content-Type' : 'Application/json', 'Authorization' : f'Bearer { self.accessToken }' }

		response = requests.get(url=api_url, headers=headers)
		return_data = response.json()

		return return_data

	'''

	def update_access_control_rule_by_id(self, group_id, name="API Update", device_type="shenxing", requestsBody=None):

		api_url = self.hostAddress + ACCESS_CONTROL_RULE_URL + '/' + str(group_id)

		headers = { 'Content-Type' : 'Application/json', 'Authorization' : f'Bearer { self.accessToken }'}

		if not requestsBody :

			requestsBody = {

				"name": name,
				"_type": device_type,
				"screenIds": []
			}

		response = requests.post(url=api_url, headers=headers, json=requestsBody)
		return_data = response.json()

		return return_data

	'''

	def delete_access_control_rule_by_id(self, group_id):

		api_url = self.hostAddress + ACCESS_CONTROL_RULE_URL + '/' + str(group_id)

		headers = { 'Content-Type' : 'Application/json', 'Authorization' : f'Bearer { self.accessToken }'}

		response = requests.delete(url=api_url, headers=headers)
		return_data = response.json()

		return return_data

	#### Company #############################

	def get_company_list(self, size=30, query=None):

		api_url = self.hostAddress + COMPANY_URL

		headers = { 'Content-Type' : 'Application/json', 'Authorization' : f'Bearer { self.accessToken }'}

		if not query :

			query = {
				'size' : size
			}

		response = requests.get(url=api_url, headers=headers, query=query)
		return_data = response.json()

		return return_data		

	### Event ###############################

	def get_event_list(self, size=30, query=None):

		api_url = self.hostAddress + EVENT_URL

		headers = { 'Content-Type' : 'Application/json', 'Authorization' : f'Bearer { self.accessToken }'}

		if not query :

			query = {
				'size' : size
			}

		response = requests.get(url=api_url, headers=headers, params=query)
		return_data = response.json()

		return return_data		

	def get_participant_list_by_event_id(self, event_id, size=30, query=None):

		api_url = self.hostAddress + EVENT_URL + f'/{event_id}' + '/event-participants'
		headers = { 'Content-Type' : 'Application/json', 'Authorization' : f'Bearer { self.accessToken }'}

		if not query :

			query = {
				'size' : size
			}

		response = requests.get(url=api_url, headers=headers, params=query)
		return_data = response.json()

		return return_data	

	### Event Application Form #############

	def get_application_form_list(self, size=30, query=None):

		api_url = self.hostAddress + EVENT_FORM_URL
		headers = { 'Content-Type' : 'Application/json', 'Authorization' : f'Bearer { self.accessToken }'}

		if not query :

			query = {
				'size' : size
			}

		response = requests.get(url=api_url, headers=headers, params=query)
		return_data = response.json()

		return return_data	

	def get_application_form_by_id(self, form_id):

		api_url = self.hostAddress + EVENT_FORM_URL + f'/{str(form_id)}'
		headers = { 'Content-Type' : 'Application/json', 'Authorization' : f'Bearer { self.accessToken }'}

		response = requests.get(url=api_url, headers=headers)
		return_data = response.json()

		return return_data			

	def register_application_from_by_id(self, form_id, image_path, attachment_path=None, requestsBody=None):

		api_url = self.hostAddress + EVENT_FORM_URL + f'/{form_id}' + '/register'
		headers = { 'Authorization' : f'Bearer { self.accessToken }'}

		if not requestsBody :

			requestsBody = {

			}

		files=[('image',('test.jpg',open(image_path,'rb'),'image/jpeg'))]

		if attachment_path :

			files.append(('attachment',('test.jpg',open(attachment_path,'rb'),'image/jpeg')))

		print(files)

		response = requests.post(url=api_url, headers=headers, data=requestsBody, files=files)
		return_data = response.json()

		return return_data

	def verify_participants_by_id(self, event_id, participant_id_list, verify=True, requestsBody=None):

		api_url = self.hostAddress + EVENT_URL + f'/{event_id}/event-participants'
		headers = { 'Content-Type' : 'Application/json', 'Authorization' : f'Bearer { self.accessToken }'}

		if not requestsBody :

			requestsBody = {

				"participantIds":participant_id_list,
				"verify":verify
			}

		response = requests.post(url=api_url, headers=headers, json=requestsBody)
		return_data = response.json()

		return return_data

	### GuardTour #############################

	def get_guard_tour_schedule(self, size=30, query=None):

		api_url = self.hostAddress + GUARD_TOUR_URL
		headers = { 'Content-Type' : 'Application/json', 'Authorization' : f'Bearer { self.accessToken }'}

		if not query :

			query = {
				'size' : size
			}

		response = requests.get(url=api_url, headers=headers, params=query, verify=False)
		try:
			return_data = response.json()
		except:
			return_data = response.text

		return return_data	 

	def get_guard_tour_schedule_by_id(self, guard_tour_id):

		api_url = self.hostAddress + GUARD_TOUR_URL + f'/{guard_tour_id}'
		headers = { 'Content-Type' : 'Application/json', 'Authorization' : f'Bearer { self.accessToken }'}

		response = requests.get(url=api_url, headers=headers, verify=False)
		return_data = response.json()

		return return_data

	def create_guard_tour_schedule(self, requestsBody=None):

		api_url = self.hostAddress + GUARD_TOUR_URL
		headers = { 'Content-Type' : 'Application/json', 'Authorization' : f'Bearer { self.accessToken }'}

		if not requestsBody :

			requestsBody = {

				"name" : "test-update",
				"personIds" : ["649121b309870f18a3c3117f"],
				"locationId" : "64c9f302d1775aeb6e871f1f",
				"isFixed" : False,
				"sunday" : True,
				"sundayTime" : ["10:00", "14:00"],
				"monday" : False,
				"tuesday" : False,
				"wednesday" : False,
				"thursday" : False,
				"friday" : False,
				"saturday" : False,
				"earlyMinutes" : 10,
				"lateMinutes" : 10
				
			}

		response = requests.post(url=api_url, headers=headers, json=requestsBody, verify=False)

		try:
			return_data = response.json()
		except:
			return_data = response.text

		return return_data

	def update_guard_tour_schedule_by_id(self, guard_tour_id, requestsBody=None):

		api_url = self.hostAddress + GUARD_TOUR_URL + f'/{guard_tour_id}'
		headers = { 'Content-Type' : 'Application/json', 'Authorization' : f'Bearer { self.accessToken }'}

		if not requestsBody :

			requestsBody = {
				"name" : "test-update",
				"personId" : "649121b309870f18a3c3117f",
				"locationId" : "64c9f302d1775aeb6e871f1f",
				"isFixed" : False,
				"sunday" : False,
				"monday" : False,
				"tuesday" : False,
				"wednesday" : False,
				"thursday" : False,
				"friday" : False,
				"saturday" : False,
				"earlyMinutes" : 10,
				"lateMinutes" : 10
				
			}

		response = requests.post(url=api_url, headers=headers, json=requestsBody, verify=False)

		try:
			return_data = response.json()
		except:
			return_data = response.text

		return return_data


	def delete_guard_tour_schedule_by_id(self, guard_tour_id):

		api_url = self.hostAddress + GUARD_TOUR_URL + f'/{guard_tour_id}'
		headers = { 'Content-Type' : 'Application/json', 'Authorization' : f'Bearer { self.accessToken }'}

		response = requests.delete(url=api_url, headers=headers, verify=False)
		return_data = response.json()

		return return_data


	### History ###############################

	def get_history_log_list(self, size=30, query=None):

		api_url = self.hostAddress + HISTORY_URL
		headers = { 'Content-Type' : 'Application/json', 'Authorization' : f'Bearer { self.accessToken }'}

		if not query :

			query = {
				'size' : size
			}

		response = requests.get(url=api_url, headers=headers, params=query, verify=False)
		return_data = response.json()

		return return_data		

	def delete_history_logs_by_id(self, log_id_list=None, requestsBody=None):	

		api_url = self.hostAddress + HISTORY_URL
		headers = { 'Content-Type' : 'Application/json', 'Authorization' : f'Bearer { self.accessToken }'}

		if not requestsBody :

			requestsBody = {"logIds":log_id_list}

		response = requests.delete(url=api_url, headers=headers, json=requestsBody)
		return_data = response.json()

		return return_data

	### People ################################

	def get_people_list(self, type='employee', size=30, page=0, query=None):

		api_url = self.hostAddress + PEOPLE_URL 

		headers = { 'Content-Type' : 'Application/json', 'Authorization' : f'Bearer { self.accessToken }'}

		if not query :

			query = {	

					'type' : type,
					'size' : size,
					'page' : page
				}


		response = requests.get(url=api_url, headers=headers, params=query)
		return_data = response.json()

		return return_data

	def get_people_by_id(self, person_id, type='employee'):

		api_url = self.hostAddress + PEOPLE_URL + f"/{person_id}"

		headers = { 'Content-Type' : 'Application/json', 'Authorization' : f'Bearer { self.accessToken }'}


		response = requests.get(url=api_url, headers=headers)
		return_data = response.json()

		return return_data

	def search_people(self, type='employee', size=30, query=None):

		api_url = self.hostAddress + SEARCH_PEOPLE_URL 

		headers = { 'Content-Type' : 'Application/json', 'Authorization' : f'Bearer { self.accessToken }'}


		if not query :

			query = {	

					'type' : type,
					'size' : size
				}


		response = requests.get(url=api_url, headers=headers, params=query)
		return_data = response.json()

		return return_data

	def update_people(self, people_id, requestsBody=None):

		api_url = self.hostAddress + PEOPLE_URL + '/' + people_id
		headers = { 'Content-Type' : 'Application/json', 'Authorization' : f'Bearer { self.accessToken }'}

		response = requests.post(url=api_url, headers=headers, json=requestsBody)
		return_data = response.json()

		return return_data

	def export_people(self, query=None):

		api_url = self.hostAddress + EXPORT_PEOPLE_URL + "?type=employee&employeeClass=vip&allCompany=true&fields=[title,email,firstName,lastName,licensePlate,mobilePhone,company,department,jobPosition,branch,region,cardId,cardName,employeeId,thaiCitizenId,passportId,enrollDate,expiredDate,employeeClass]"
		headers = { 'Content-Type' : 'Application/json', 'Authorization' : f'Bearer { self.accessToken }'}

		response = requests.get(url=api_url, headers=headers)
		return_data = response.json()

		return return_data

	def upload_person_image(self, person_id, image_path):

		api_url = self.hostAddress + PEOPLE_URL + f"/{person_id}/photo/" 

		headers = {  'Authorization' : f'Bearer { self.accessToken }'}

		files = {'photo': open(image_path, 'rb')}
		# files=[  ('photo',('image.png',open(image_path,'rb'),'image/png'))]

		response = requests.post(url=api_url, files=files, headers=headers)

		return_data = response.json()

		return return_data

import json

if __name__ == '__main__':


	face48 = Face48(hostAddress='https://dev.face48.com', username='iyo@nvk.co.th', password='P@ssw0rd!234')
	# face48 = Face48(hostAddress='http://10.250.81.58', username='enco_admin', password='EnCo@2021')
	# face48 = Face48(hostAddress='http://10.10.10.97', username='admin', password='P@ssw0rd@NMU')
	# face48 = Face48(hostAddress='https://face48.vajira.ac.th', username='admin', password='P@ssw0rd2022')
	# face48 = Face48(hostAddress='http://192.168.33.45', username='iyo@nvk.co.th', password='P@ssw0rd!234')

	print(face48.login())

	# print(face48.sudo_face_scan('/7vqbx9'))
	# print(face48.get_access_control_group_list())
	# print(face48.create_access_control_group())
	# print(face48.get_access_control_group_by_id('643e66a9f05fdf6356691b54'))
	# print(face48.update_access_control_group_by_id('643e6999132f4273a3637d21'))
	# print(face48.delete_access_control_group_by_id('643e66a9f05fdf6356691b54'))

	# print(face48.get_event_application_form_list())

	# print(face48.get_access_control_rule_list())

	query = {
		"success":True,
		# "summary":True,
		"size":30,
		"page":1,
		"start_id":"64a7da066259cd8d171392e8",
		'order_by' : 'desc',
		# "startDate":'2023-06-14 00:00',
		# "endDate":"2023-06-15 06:59"
	}
	# print(json.dumps(face48.get_history_log_list(query=query), indent=4))
	# print(face48.delete_history_logs_by_id(log_id_list=['64333e9dd77a506b1f77659f']))

	# print(face48.export_people())

	print(face48.get_people_by_id("652f5d8b050ccedaa8337c2a")['data'])

	# print(face48.get_people_list(query={'type' : 'employee','size' : 30, 'employeeId' : 'NVK48'}))
	# print(face48.search_people(query={'type' : 'employee','size' : 30, 'employeeId' : 'NVK48'}))

	print(face48.logout())





	