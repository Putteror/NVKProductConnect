from Face48.Face48 import *
from Shenxing.shenxing_7 import *
import pandas as pd

face48 = Face48(hostAddress='http://172.21.35.249', username='admin', password='P@ssw0rd2023')
shenxing = Shenxing(hostAddress='http://172.21.35.248', username='admin', password='nvk12345')
print(face48.login())
print(shenxing.login())


### Shenxing #######################################################

check_all_obj = shenxing.get_person_list(limit=1)

all_obj = check_all_obj['paging']['total']

all_page = int(all_obj / 100) + 1

person_id_list_in_shenxing = []

for page in range(0,all_page) :
	print(page*100)
	person_list = shenxing.get_person_list(limit=100, offset=page*100)['data']
	for person in person_list :

		person_id_list_in_shenxing.append(person['id'])

####################################################################

### Face 48 ########################################################

resp_get_person_in_face48 = face48.get_people_list(query={'type' : 'employee','size' : 1400})

person_list = resp_get_person_in_face48['data']
person_id_list_in_face48 = []

for person in person_list :

	person_id_list_in_face48.append(person['id'])

###################################################################

loss_person_id_list = []
loss_person_info_list = []

for face48_person_id in person_id_list_in_face48 :

	if face48_person_id in person_id_list_in_shenxing :

		loss_person_id_list.append(face48_person_id)
		person_info = {}
		person_info_response = face48.get_people_by_id("652f5d8b050ccedaa8337c2a")['data']
		person_info['employeeId'] = person_info_response['employeeId']
		person_info['firstName'] = person_info_response['firstName']
		person_info['lastName'] = person_info_response['lastName']
		person_info['company'] = person_info_response['company']
		loss_person_info_list.append(person_info)

df = pd.DataFrame(loss_person_info_list)

# Specify the output file name (e.g., 'employee_data.xlsx')
output_file = 'employee_data.xlsx'

# Save the DataFrame to an Excel file
df.to_excel(output_file, index=False)  # index=False to exclude the index column



print(loss_person_info_list)
print(face48.logout())
print(shenxing.logout())
