from shenxing_7 import *
from Face48 import *

PERSON_TYPE = ['staff', 'visitor', 'all']

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

	def delete_person_by_id_list(self, person_id_list):

		resp_list = []

		for person_id in person_id_list :

			resp_data = self.delete_person_by_id(person_id=person_id)
			resp_list.append(resp_data)

		return resp_list


def delete_all_employee_from_shenxing_7_inch(shenxing_object):

	shenxing_object.login()

	staff_list = shenxing_object.get_person_list_from_type(personType='staff')

	staff_id_list = extract_value_from_field_name_in_json_list_to_new_list(json_list=staff_list, field_name="id")
	print("delete list id : ", staff_id_list)

	delete_person_list = shenxing_object.delete_person_by_id_list(person_id_list=staff_id_list)
	print(delete_person_list)

	shenxing_object.logout()

def delete_all_person_not_have_in_face48(shenxing_object, face48_object):

	shenxing_person_list = shenxing_object.get_person_list_from_type(personType='all')
	shenxing_person_id_list = extract_value_from_field_name_in_json_list_to_new_list(json_list=shenxing_person_list, field_name="id")

	print(shenxing_person_id_list, len(shenxing_person_id_list))

	for shenxing_person_id in shenxing_person_id_list :

		face48_person_json = face48_object.get_people_by_id(shenxing_person_id)

		if face48_person_json['code'] != 200 :

			shenxing_object.delete_person_by_id(shenxing_person_id)
			print("delete : ", shenxing_person_id)




if __name__ == '__main__':

	shenxing_object = Shenxing(hostAddress='http://192.168.33.107', username='admin', password='nvk12345')
	face48_object = Face48(hostAddress='https://dev.face48.com', username='iyo@nvk.co.th', password='P@ssw0rd!234')

	shenxing_object.login()
	face48_object.login()
	
	delete_all_person_not_have_in_face48(shenxing_object, face48_object)


	shenxing_object.logout()
	face48_object.logout()