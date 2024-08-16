import pandas as pd
import json

def read_excel_file_to_json_list(excelPath):

	df = pd.read_excel(excelPath)

	excel_json_str = df.to_json(orient='records')
	excel_json = json.loads(excel_json_str)

	return excel_json

def export_duplicate_field_in_excel(excelPath, fieldNameList):

	data_object_list = read_excel_file_to_json_list(excelPath)
	key_value_list = []
	duplicate_key_value_list = []

	duplicate_object_list = []

	for data_object in data_object_list :

		key_value_str = ""

		for filename in fieldNameList :

			key_value_str = key_value_str + str(data_object[filename])

		if ( key_value_str in key_value_list ) and ( key_value_str not in duplicate_key_value_list ) :

			return_data_object = {}

			for filename in fieldNameList :

				return_data_object[filename] = str(data_object[filename])

			duplicate_object_list.append(return_data_object)
			duplicate_key_value_list.append(key_value_str)

		key_value_list.append(key_value_str)

	duplicate_object_df = pd.DataFrame(duplicate_object_list)
	duplicate_object_df.to_excel('data.xlsx', index=False)

def export_same_value_in_excel(excelPath1, excelPath2, fieldNameList):

	data_object_list = read_excel_file_to_json_list(excelPath1)
	data_ref_object_list = read_excel_file_to_json_list(excelPath2)

	same_object_list = []


	### Set Data Ref Key Value #################

	key_value_ref_list = []

	for data_ref_object in data_ref_object_list :

		key_value_ref_str = ""

		for filename in fieldNameList :

			key_value_ref_str = key_value_ref_str + str(data_ref_object[filename])

		key_value_ref_list.append(key_value_ref_str)

	print(key_value_ref_list)

	### Compare and export ###################

	for data_object in data_object_list :

		key_value_str = ""

		print(data_object['firstName'])

		for filename in fieldNameList :

			key_value_str = key_value_str + str(data_object[filename])

		if key_value_str in key_value_ref_list :

			print(key_value_str, key_value_ref_str)

			same_object_list.append(data_object)

	same_object_df = pd.DataFrame(same_object_list)
	same_object_df.to_excel('same_data.xlsx', index=False)













if __name__ == '__main__':

	# employee_list = export_duplicate_field_in_excel(excelPath="Employee.xlsx", fieldNameList=["firstName", "lastName", "employeeId", "cardId", "company", "department"])

	export_same_value_in_excel(excelPath1="Employee.xlsx", excelPath2="data.xlsx", fieldNameList=["firstName", "lastName", "employeeId", "cardId", "company", "department"])
