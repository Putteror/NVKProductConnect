from koala import *
import pandas as pd

# koala = Koala(hostAddress='http://192.168.20.102/', username='tor@nvk.co.th', password='nVk123456')
koala = Koala(hostAddress='http://172.21.1.16/', username='admin@ddc.mail.go.th', password='admin1234')

def get_all_person_list(export_to_excel=False):

	first_get_person_list_data = koala.get_person_list(query={"size":1})

	person_list_count = first_get_person_list_data['page']['count']

	all_person_list_data = koala.get_person_list(query={"size":person_list_count})

	count = 0

	no_face_person_data_list = []

	for person_data in all_person_list_data['data'] :


		if len(person_data['photos']) == 0 :

			no_face_person_data = {}
			
			no_face_person_data['name'] = person_data['name']
			no_face_person_data['employeeId'] = person_data['extra_id']
			no_face_person_data['jobPosition'] = person_data['title']

			no_face_person_data_list.append(no_face_person_data)

			count = count +1

	print(count)
	print(no_face_person_data_list)

	if export_to_excel == True :

		# Create a DataFrame
		df = pd.DataFrame(no_face_person_data_list)

		# Write DataFrame to Excel
		df.to_excel('no_photo_person.xlsx', index=False) 

if __name__ == '__main__':

	print(555)
	
	get_all_person_list(export_to_excel=True)