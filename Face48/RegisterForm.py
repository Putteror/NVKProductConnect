from face48 import Face48
from helper import *

face48 = Face48(hostAddress='http://192.168.33.56', username='admin', password='P@ssw0rd2023')
face48.login()



def get_form_field(form_id):

	get_form_info = face48.get_application_form_by_id(form_id)

	application_form_data = get_form_info['data']

	field_list = []

	for field in application_form_data : 

		if ( 'field' in field ) and ( 'Placeholder' not in field ) and ( 'Required' not in field ):

			if application_form_data[field] :
				field_name = field.replace('field','').lower()
				field_list.append(field_name)

	return field_list
	

def register_form_again_all_participant():

	person_image_folder = 'assets/event/person/'
	attachment_image_folder = 'assets/event/attachment/'

	event_participant_list = get_all_participants()

	for event_participant in event_participant_list :

		print(event_participant['firstName'])

		register_form_id = event_participant['applicationFormId']

		field_list = get_form_field(register_form_id)

		requestsBody = {}
		attachment_path = None
		image_path = None

		for field in field_list:

			if field == 'arrivaltime' :

				time_obj = datetime.datetime.strptime(event_participant['event_participant_arrival_time'], "%Y-%m-%d %H:%M:%S")
				requestsBody['arrivalTime'] = time_obj.strftime("%Y-%m-%d %H:%M")

			if field == 'attachment' : 

				attachment_path = attachment_image_folder + str(event_participant['id']) + '.jpg'
				base64_to_image_file(base64_data=event_participant['attachment'], path=attachment_path)

			if field == 'company' :

				requestsBody['company'] = event_participant['company']['name']

			if field == 'department' : 

				requestsBody['department'] = event_participant['department']['name']


			if field == 'departtime' :

				time_obj = datetime.datetime.strptime(event_participant['event_participant_depart_time'], "%Y-%m-%d %H:%M:%S")
				requestsBody['departTime'] = time_obj.strftime("%Y-%m-%d %H:%M")

			if field == 'firstlastname' : 

				requestsBody['firstLastName'] = event_participant['firstName'] + ' ' + event_participant['lastName']

			if field == 'mobile' : 

				requestsBody['mobile'] = event_participant['mobilePhone']

			if field == 'visitee' :

				requestsBody['visitee'] = event_participant['visitee']

			if field == 'visitingpurpose' :

				requestsBody['visitingPurpose'] = event_participant['visitPurpose']

		image_path = person_image_folder + str(event_participant['id']) + '.jpg'
		base64_to_image_file(base64_data=event_participant['photos'][0]['image'], path=image_path)

		print(requestsBody)

		response = face48.register_application_from_by_id(form_id=register_form_id, image_path=image_path, attachment_path=attachment_path, requestsBody=requestsBody)

		print(response)



def get_all_participants():

	get_event_response = face48.get_event_list()

	event_list = get_event_response['data']['events']

	event_participant_list = []

	for event in event_list :

		event_id = event['id']

		get_participant_response = face48.get_participant_list_by_event_id(event_id)

		participant_list = get_participant_response['data']['data']

		event_participant_list.extend(participant_list)

	return event_participant_list



	






	


if __name__ == '__main__':

	print(register_form_again_all_participant())
	
	face48.logout()
