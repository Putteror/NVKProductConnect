from shenxing_7 import *

PERSON_TYPE = ['staff', 'visitor']

def extract_value_from_field_name_in_json_list_to_new_list(json_list, field_name):

	new_list = []


	for json_data in json_list :

		value = json_data[field_name]

		new_list.append(value)

	return new_list

class Shenxing(Shenxing):

	def get_person_list_from_type(self, personType):

		if personType in PERSON_TYPE :

			all_person_list = []

			limit_value = 100
			offset_value = 0

			RUNNING = True
			
			while RUNNING is True :

				resp_data = self.get_person_list(limit=limit_value, offset=offset_value)

				person_list = resp_data['data']
				
				if len(person_list) > 0 :

					for person_json in person_list :

						if person_json['recognition_type'] == personType :

							all_person_list.append(person_json)

				elif len(person_list) <= 0 :

					RUNNING = False

				offset_value = offset_value + limit_value

			return all_person_list

		elif personType not in PERSON_TYPE :

			return "Incorrect person type"

	def delete_person_by_id_list(self, person_id_list):

		resp_list = []

		for person_id in person_id_list :

			resp_data = self.delete_person_by_id(person_id=person_id)
			resp_list.append(resp_data)

		return resp_list


if __name__ == '__main__':
	
	shenxing_object = Shenxing(hostAddress='http://192.168.33.107', username='admin', password='nvk12345')

	shenxing_object.login()

	staff_list = shenxing_object.get_person_list_from_type(personType='staff')

	staff_id_list = extract_value_from_field_name_in_json_list_to_new_list(json_list=staff_list, field_name="id")
	print("delete list id : ", staff_id_list)

	delete_person_list = shenxing_object.delete_person_by_id_list(person_id_list=staff_id_list)
	print(delete_person_list)

	shenxing_object.logout()



