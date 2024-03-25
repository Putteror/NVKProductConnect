from Face48 import *
from koala import *
import os

def get_image_name_list_from_folder(folder_path):

	file_paths = []
	# Iterate over all files in the folder
	for file_name in os.listdir(folder_path):
		# Check if it's a file (not a directory)
		if os.path.isfile(os.path.join(folder_path, file_name)):
			# Join the folder path with the file name to get the full file path
			file_paths.append(os.path.join(folder_path, file_name))
	return file_paths


def check_have_photo_in_koala(koala_subject_id, koala_object):

	person_information = koala_object.get_person_by_id(subject_id=koala_subject_id)

	try:

		person_image_list = person_information['data']['photos'] 

		if len(person_image_list) > 0 :

			return True

		else :

			return False

	except Exception as e:

		print(str(e))

		return False


def get_person_data_from_face48(employee_id, face48_object):


	query = {
			'type' : "employee",
			'size' : 1,
			'employeeId' : employee_id
	}

	resp = face48_object.search_people(query=query)

	person_data = resp['data'][0]

	return person_data


def upload_folder_image_to_face48_only_not_have_face_in_koala(face48_object, koala_object, folder_path):


	file_path_list = get_image_name_list_from_folder(folder_path)

	count = 0

	for file_path in file_path_list :

		# file_path = "C:/Work/NVK48/UIH/picture_recheck\\1100200803520.jpg"

		file_name = os.path.basename(file_path)
		employee_id = os.path.splitext(file_name)[0]

		person_data = get_person_data_from_face48(employee_id, face48_object)
		have_photo_in_koala = check_have_photo_in_koala(person_data['subject_id'], koala_object)

		print(person_data['firstName'], person_data['lastName'], person_data['employeeId'], have_photo_in_koala)

		if not have_photo_in_koala :

			count = count + 1

			upload_image_resp = face48_object.upload_person_image(person_id=person_data['id'], image_path=file_path)
			print(upload_image_resp)
			print("add : ", count)

	return count




if __name__ == '__main__':

	koala_object = Koala(hostAddress='http://172.21.1.16/', username='admin@ddc.mail.go.th', password='admin1234')
	face48_object = Face48(hostAddress='http://172.21.1.17', username='admin', password='P@ssw0rd2024')

	face48_object.login()

	folder_path = "C:/Work/NVK48/UIH/picture_16_02_2567"
	
	upload_folder_image_to_face48_only_not_have_face_in_koala(face48_object, koala_object, folder_path)
