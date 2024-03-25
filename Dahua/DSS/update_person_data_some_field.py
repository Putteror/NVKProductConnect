from dssAPI import *

dss = DSS(hostAddress="https://192.168.80.167", username="system", password="Dpu12345")


def get_all_person_id_from_dss_by_group(groupCode=None):

	if groupCode is None :

		group_code_list = []

		all_person_group = dss.get_person_group_list()['data']['results']
		
		for person_group in all_person_group :

			group_code_list.append(person_group['orgCode'])

		print( f"Put some groupCode in list {group_code_list}")

		return group_code_list

	else :

		person_id_list = []

		all_person_list = dss.get_person_list(groupCode=groupCode, pageSize=1000)['data']['pageData']

		for person in all_person_list :

			person_id_list.append(person['baseInfo']['personId'])


		return person_id_list


def count_person_not_have_finger():

	person_id_list = get_all_person_id_from_dss_by_group(groupCode="001")

	total = 0
	have_finger = 0
	not_have_finger = 0
	have_finger_expire = 0
	not_have_finger_expire = 0
	result = {}

	for person_id in person_id_list :

		total += 1
		print(total)

		person_resp = dss.get_person_by_id(person_id)

		# print(person_resp)

		finger_data = person_resp['data']['authenticationInfo']['fingerprints']
		expire_data = person_resp['data']['authenticationInfo']['expired']
		person_firstname = person_resp['data']['baseInfo']['firstName']
		person_lastname = person_resp['data']['baseInfo']['lastName']


		print(person_firstname)
		# print(dss.update_person(personId=person_id, firstName=person_firstname, lastName=person_lastname, fingerprints=finger_data))




		if len(finger_data) > 0 :

			have_finger += 1

			if expire_data == "1" :

				have_finger_expire += 1


		elif len(finger_data) <= 0 :

			not_have_finger += 1

			if expire_data == "1" :

				not_have_finger_expire += 1

				# print(dss.update_person(personId=person_id, firstName=person_firstname, lastName=person_lastname))

		dss.keep_alive()

	result['total'] = total
	result['have_finger'] = have_finger
	result['not_have_finger'] = not_have_finger
	result['have_finger_expire'] = have_finger_expire
	result['not_have_finger_expire'] = not_have_finger_expire

	print(result)


if __name__ == '__main__':
	
	count_person_not_have_finger()

	{'total': 803, 'have_finger': 657, 'not_have_finger': 146, 'have_finger_expire': 0, 'not_have_finger_expire': 1}

