import requests
from requests.auth import HTTPDigestAuth
import base64
from DSS.dssAPI import DSS
from Pad.padAPI import Dahua
import json

DAHUA_PAD_ADDRESS = "http://192.168.33.31"
DAHUA_PAD_USERNAME = "admin"
DAHUA_PAD_PASSWORD = "nVk12345"

DSS_ADDRESS = "https://192.168.11.250"
DSS_USERNAME = "system"
DSS_PASSWORD = "nVk12345"

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

	for personId in personIds:

		response = pad.get_person_fingerprint(personId=personId)

		status = response.status_code
		
		if status == 200 :

			fingerprint_code = parse_response_content(response.content)['FingerprintData']

			print(fingerprint_code)



if __name__ == '__main__':
	
	# print((get_person_fingerprint_from_pad("03727333")))

	# sync_fingerprint_by_person_group(groupCode="001")

	person_id_list = get_all_person_id_from_dss_by_group(groupCode="001007")

	print(sync_fingerprint_by_person_id_list(person_id_list))