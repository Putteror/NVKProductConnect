from face48 import *

face48 = Face48(hostAddress='http://10.250.81.58', username='enco_admin', password='P@ssw0rd2021')



def convert_people_data_to_payload(data):

   payload = {
      "_type": data['_type'],
      "title": data['title']['id'] if data['title'] is not None else None,
      "firstName": data['firstName'],
      "middleName": data['middleName'],
      "lastName": data['lastName'],
      "nickname": data['nickname'],
      "gender": data['gender'],
      "birthDay":data['birthDay'],
      "thaiCitizenId": data['thaiCitizenId'],
      "passportId": data['passportId'],
      "martialStatus": data['martialStatus'],
      "nationality": data['nationality'],
      "bloodType": data['bloodType'],
      "mobilePhone": data['mobilePhone'],
      "workPhone": data['workPhone'],
      "email": data['email'],
      "licensePlate": data['licensePlate'],
      "fullAddress": data['fullAddress'],
      "address":{
         "civicNumber": data['address']['civicNumber'],
         "buildingName": data['address']['buildingName'],
         "roomNumber": data['address']['roomNumber'],
         "floorNumber": data['address']['floorNumber'],
         "alley": data['address']['alley'],
         "street": data['address']['street'],
         "subDistrict": data['address']['subDistrict'],
         "district": data['address']['district'],
         "province": data['address']['province'],
         "postcode": data['address']['postcode']
      } if data['address'] else None,
      "company": data['company']['id'] if data['company'] is not None else None,
      "department": data['department']['id']  if data['department'] is not None else None,
      "jobPosition": data['jobPosition']['id'] if data['jobPosition'] is not None else None,
      "workPhoneExtension": data['workPhoneExtension'],
      "ssno": data['ssno'],
      "employeeId": data['employeeId'],
      "employeeStatus": data['employeeStatus'],
      "employmentType": data['employmentType'],
      "employeeClass": data['employeeClass'],
      "enrollDate": data['enrollDate'],
      "exitDate": data['exitDate'],
      "expiredDate": data['expiredDate'],
      "division": data['division'],
      "signature":data['signature'],
      "description": data['description'],
      "group": data['group'],
      "visitee": data['visitee'],
      "visitPurpose": data['visitPurpose'],
      # "visitorCategory": data['visitorCategory'],
      "reason": data['reason'],
      "accessControlEnabled": data['accessControlEnabled'],
      "accessControlDisabled": data['accessControlDisabled'],
      "accessControlRuleIds": [ acr['id'] for acr in data['accessControlRules'] ],
      "cardId": data['cardId'],
      "cardName": data['cardName'],
      # "ward": data['ward'],
      # "useDynamicShift": data['useDynamicShift'],
      "attendanceTimeIds":[ _['id'] for _ in data['attendanceTime'] ],
      "holidayGroupId": data['holidayGroup'],
      "leaveTypeListId": data['leaveTypeList'],
      "branchId": data['branch']['id'] if data['branch'] else None,
      "disabledHistoryLog": data['disabledHistoryLog'],
      "disabledTimeAttendance": data['disabledTimeAttendance'],
      "disabledCheckInRecord": data['disabledCheckInRecord'],
      "userDefinedValues": data['userDefinedValues'],
      # "wifiUsername": data['wifiUsername'],
      # "wifiPassword": data['wifiPassword'],
      # "networkPolicyId": data['networkPolicy'],
      # "hikCentralAccessLevelListIds": [ _['id'] for _ in data['hikCentralAccessLevelLists'] ]  if data['hikCentralAccessLevelLists'] else None,
      # "minmoeDeviceGroupIds":[
         
      # ]
   }

   return payload


def replace_employee_id_from_employee_id_group(employee_id, replace_employee_id):

   face48.login()

   query = {

            'type' : 'employee',
            'size' : 30, 
            'employeeId' : employee_id
   }

   response = face48.search_people(query=query)
   # print(response['data'])
   people_list = response['data']

   for people in people_list :

      # try :

      people_id = people['id']

      payload = convert_people_data_to_payload(people)

      # print(payload)

      payload['employeeId'] = payload['employeeId'].replace(employee_id, replace_employee_id)

      face48.update_people( people_id=people_id, requestsBody=payload)

      print(people_id)

      # except Exception as e: 

      #    print(people['id'], e)

   face48.logout()



if __name__ == '__main__':
   
   replace_employee_id_from_employee_id_group('PTTGC2601', 'GC2601')



