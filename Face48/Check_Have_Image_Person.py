from Face48 import *
import pandas as pd

face48 = Face48(hostAddress='http://172.21.1.17', username='admin', password='P@ssw0rd2024')

face48.login()

def get_have_face_image_person(export_to_excel=False):

	people_list_page_total = face48.get_people_list(size=100, page=1)['page']['total']

	no_face_person_list = []

	for page in range(0, people_list_page_total) :

		print(page, page*100)

		people_list = face48.get_people_list(size=100, page=page)

		for people in people_list['data'] :

			no_face_person_json = {}

			if len(people['photos']) > 0 :

				no_face_person_json['firstName'] = people['firstName']
				no_face_person_json['lastName'] = people['lastName']
				no_face_person_json['employeeId'] = people['employeeId']
				no_face_person_json['jobPosition'] = people['jobPosition']['name'] if people['jobPosition'] else None

				no_face_person_list.append(no_face_person_json)



	print(no_face_person_list)
	print(len(no_face_person_list))

	if export_to_excel == True :

		# Create a DataFrame
		df = pd.DataFrame(no_face_person_list)

		# Write DataFrame to Excel
		df.to_excel('have_photo_person_face48.xlsx', index=False) 


if __name__ == '__main__':

	print(555)
	
	get_have_face_image_person(export_to_excel=True)