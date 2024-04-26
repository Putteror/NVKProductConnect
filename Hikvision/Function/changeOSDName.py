import pandas as pd
import requests
import xmltodict
import json


##########################################################################
#### Global Function #####################################################
##########################################################################

def convert_xml_to_json(xml_string):

    xml_dict = xmltodict.parse(xml_string)
    json_data = json.dumps(xml_dict, indent=4)

    return json_data

##########################################################################
##########################################################################
##########################################################################

class Camera: # Call This Class For Send API To Hikvision Camera

    def __init__(self, hostAddress, username, password):

        self.hostAddress = hostAddress
        self.username = username
        self.password = password
        self.auth = requests.auth.HTTPDigestAuth(username, password)

    def update_camera_osd_name(self, cameraName, cameraChannel=1):

        api_path = "/ISAPI/System/Video/inputs/channels"

        api_url = self.hostAddress + api_path + f'/{cameraChannel}'

        requestsBody = f""" 

                <VideoInputChannel>
                <id>1</id>
                <inputPort>1</inputPort>
                <name>{cameraName}</name>
                <videoFormat>PAL</videoFormat>
                </VideoInputChannel>
                                    
                """

        response = requests.put(url=api_url, data=str(requestsBody), auth=self.auth)

        response_json = convert_xml_to_json(response.text)
        return_data = json.loads(response_json)

        return return_data


def change_camera_name_from_excel(excelPath): # Function to change camera OSD Name from excel

    result_list = []

    df = pd.read_excel(excelPath)

    insert_camera_data_list = df.to_json(orient='records')
    insert_camera_data_list = json.loads(insert_camera_data_list)

    for insert_camera_data in insert_camera_data_list :

        ip_address      = insert_camera_data['IP Address']
        username        = insert_camera_data['Username']
        password        = insert_camera_data['Password']
        camera_name_osd = insert_camera_data['Camera Name']

        host_address    = f"http://{ip_address}"

        camera_object = Camera(hostAddress=host_address, username=username, password=password)
        resp = camera_object.update_camera_osd_name(cameraName=camera_name_osd)

        result = {}
        result['ipAddress'] = ip_address

        try:
            result['status'] = resp['ResponseStatus']['statusString']
        except:
            result['status'] = resp

        result_list.append(result)

    print(result_list)

    return result_list

if __name__ == '__main__':

    change_camera_name_from_excel(excelPath='CameraIPNameList.xlsx')