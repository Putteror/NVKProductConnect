from Face48 import *
import requests

face48 = Face48(hostAddress='https://dev.face48.com', username='iyo@nvk.co.th', password='P@ssw0rd!234')
face48.login()

def test_face48_api_function(response_data):

	try:

		code_status = response_data['code']
		json_data = response_data['data']
		description = response_data['desc']

		if code_status != 200 :
			return response_data

		return code_status

	except:

		return response_data


class GuardTour:

	def __init__(self):

		self.path = ''

	def delete_all(self):

		guard_tour_list = face48.get_guard_tour_schedule()['data']

		if guard_tour_list:

			for guard_tour in guard_tour_list :
				print(guard_tour)
				delete = face48.delete_guard_tour_schedule_by_id(guard_tour['id'])
				print(delete)

	def test_flow(self, requestsBody=None):

		requestsBody = {

				"personId" : "649121b309870f18a3c3117f",
				"locationId" : "6317009e3c8b43633c544f67",
				"isFixed" : True,
				"fixedDateTime" : "2022-02-01 22:22",
				"sunday" : True,
				"sundayTime" : ["10:00", "22:00"],
				"monday" : False,
				"mondayTime" : ["10:00", "22:00"],
				"tuesday" : True,
				"tuesdayTime" : ["10:00", "22:00"],
				"wednesday" : False,
				"wednesdayTime" : [],
				"thursday" : False,
				"friday" : False,
				"saturday" : False,
				"earlyMinutes" : 0,
				"lateMinutes" : 420
				
			}

		try:

			create_guard_tour = face48.create_guard_tour_schedule(requestsBody)
			print(test_face48_api_function(create_guard_tour))

			get_guard_tour = face48.get_guard_tour_schedule()
			print(test_face48_api_function(get_guard_tour))

			get_guard_tour_by_id = face48.get_guard_tour_schedule_by_id(create_guard_tour['data']['id'])
			print(test_face48_api_function(get_guard_tour_by_id))

			requestsBody['wednesday'] = True 
			update_guard_tour_by_id = face48.update_guard_tour_schedule_by_id(create_guard_tour['data']['id'], requestsBody)
			print(test_face48_api_function(update_guard_tour_by_id))

			delete_guard_tour_by_id = face48.delete_guard_tour_schedule_by_id(create_guard_tour['data']['id'])
			print(test_face48_api_function(delete_guard_tour_by_id))

		except Exception as e :

			print(e)

		return "finish"

if __name__ == '__main__':

	
	guard_tour = GuardTour()

	print(guard_tour.test_flow())
	# print(guard_tour.delete_all())

	face48.logout()


