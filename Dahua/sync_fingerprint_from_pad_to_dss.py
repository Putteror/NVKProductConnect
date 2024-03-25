import requests
from requests.auth import HTTPDigestAuth
import base64
from DSS.dssAPI import DSS
from Pad.padAPI import Dahua
import json


DAHUA_PAD_ADDRESS = "http://192.168.151.36"
DAHUA_PAD_USERNAME = "admin"
DAHUA_PAD_PASSWORD = "dpu!2345"

DSS_ADDRESS = "https://192.168.80.167"
DSS_USERNAME = "system"
DSS_PASSWORD = "Dpu12345"

dss = DSS(hostAddress=DSS_ADDRESS, username=DSS_USERNAME, password=DSS_PASSWORD)
pad = Dahua(hostAddress=DAHUA_PAD_ADDRESS, username=DAHUA_PAD_USERNAME, password=DAHUA_PAD_PASSWORD)

def json_print(data):
	print(json.dumps(data, indent=4))

def parse_response_content(content):
    lines = content.decode('utf-8').split('\r\n')
    parsed_data = {}

    for line in lines:
        parts = line.split('=')
        if len(parts) == 2:
            key = parts[0]
            value = parts[1]
            parsed_data[key] = value

    return parsed_data


def get_person_fingerprint_from_pad(personId):

	get_person_fingerprint_path = "/cgi-bin/AccessFingerprint.cgi?action=get"
	get_person_fingerprint_url = DAHUA_PAD_ADDRESS + get_person_fingerprint_path

	query = {

		"UserID" : str(personId)

	}

	get_person_fingerprint_response = requests.get( url=get_person_fingerprint_url, auth=HTTPDigestAuth(DAHUA_PAD_USERNAME, DAHUA_PAD_PASSWORD), params=query )

	return parse_response_content(get_person_fingerprint_response.content)['FingerprintData']


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




def sync_fingerprint_by_person_id_list(personIds):

	count = 0

	for personId in personIds:

		print(personId)

		response = pad.get_person_fingerprint(personId=personId)
		person_information = dss.get_person_by_id(personId)
		# print(response)

		try:

			person_firstname = person_information['data']['baseInfo']['firstName']
			person_lastname = person_information['data']['baseInfo']['lastName']

		except :

			print(person_information)

		print(person_firstname, person_lastname)


		status = response.status_code
		
		if status == 200 : ### if have finger in pad

			count = count + 1

			print(f"have finger {count}")

			fingerprint_code = parse_response_content(response.content)['FingerprintData']

			count_fingerprint = int(len(fingerprint_code) / 1080 )
			fingerprint_list = []

			for i in range(count_fingerprint):

				fingerprint_list.append(fingerprint_code[(i*1080):((i+1)*1080)])


			# json_print(dss.get_person_by_id("555"))

			if ( personId == "430607" ) or ( personId == "601162" ):

				print(dss.update_person(personId=personId, firstName=person_firstname, lastName=person_lastname, fingerprint_list=fingerprint_list))

		dss.keep_alive()

if __name__ == '__main__':
	
	person_id_list = get_all_person_id_from_dss_by_group(groupCode="001")

	print(person_id_list)

	print(sync_fingerprint_by_person_id_list(person_id_list))