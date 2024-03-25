from shenxing_7 import *

PERSON_TYPE = ['staff', 'visitor', 'blacklist', 'all']

class Shenxing(Shenxing):

	def get_person_list_from_type(self, personType):

		if personType in PERSON_TYPE :

			all_person_list = []

			RUNNING = True

			limit_value = 100
			offset_value = 0

			while RUNNING is True :

				resp_data = self.get_person_list(limit=limit_value, offset=offset_value)

				person_list = resp_data['data']
				
				if len(person_list) > 0 :

					for person_json in person_list :

						if personType == 'all' :

							all_person_list.append(person_json)

						elif person_json['recognition_type'] == personType :

							all_person_list.append(person_json)


				elif len(person_list) <= 0 :

					RUNNING = False

				offset_value = offset_value + limit_value

			return all_person_list

		elif personType not in PERSON_TYPE :

			return "Incorrect person type"

if __name__ == '__main__':
	
	shenxing_object = Shenxing(hostAddress='http://192.168.33.107', username='admin', password='nvk12345')

	shenxing_object.login()

	
	person_list = shenxing_object.get_person_list_from_type(personType='all')
	print(person_list)


	shenxing_object.logout()
