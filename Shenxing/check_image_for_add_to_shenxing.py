from shenxing_7 import *
import glob
from PIL import Image
import os
import pandas as pd

def get_all_file_in_folder(folder_path, file_type=None):

	file_path_list = []

	if file_type is None :
		file_paths = glob.glob(f"{folder_path}/*")
	else :
		file_paths = glob.glob(f"{folder_path}/*.{file_type}")

	for path in file_paths:
		file_path_list.append(path)

	return file_path_list

def resize_and_save_image(input_path, output_path):

	try:

		# Open the image
		image = Image.open(input_path)

		# Resize the image to 400x400 pixels
		resized_image = image.resize((400, 400))

		# Save the resized image to the output path
		resized_image.save(output_path)

	except Exception as e:

		print(f"An error occurred: {str(e)}")


def resize_all_image_in_folder_and_save_to_new_folder(original_folder_path, new_folder_path, image_type='jpg'):

	file_path_list = get_all_file_in_folder(original_folder_path, image_type)

	count = 0
	error_list = {}
	result = []

	for file_path in file_path_list :

		try:

			count = count + 1

			file_name = os.path.basename(file_path)
			new_path = f'{new_folder_path}/{file_name}'

			resize_and_save_image(file_path, new_path)

			extract_resp =  shenxing.extract_image(image_path=new_path)
			extract_result = extract_resp['result']
			result.append(extract_result)

			if extract_result != 0 :

				error_list[new_path] = f" Shenxing Denied {extract_result}"

		except:

			try:
				error_list[file_path] = extract_resp
			except:
				error_list[file_path] = 'Cannot resize'

	return result, error_list

def comparison_file_name_and_excel(folder_path, excel_path, sheet_name='Sheet1', file_type="jpg"):

	df = pd.read_excel(excel_path, sheet_name=sheet_name)

	employee_id_list = df["employeeId"].tolist()

	for i in range(len(employee_id_list)):
		employee_id_list[i] = str(employee_id_list[i])

	image_path_list = get_all_file_in_folder(folder_path, file_type=file_type)

	for image_path in image_path_list :

		image_name = os.path.basename(image_path).split(".")[0]

		# try:
		# 	new_image_name = remove_leading_zeros(image_name)
		# 	os.rename(image_path, f"C:/Work/NVK48/IFS/TBKK/EmployeeData/EmployeeFaceImage/change/{new_image_name}.jpg")
		# except:
		# 	pass

		if image_name not in employee_id_list :

			print(image_name, "not in")
			os.remove(image_path)

		else:

			print(image_name)

def remove_leading_zeros(s):
    return str(int(s))



if __name__ == '__main__':

	shenxing = Shenxing(hostAddress='http://192.168.33.108', username='admin', password='nvk12345')
	print(shenxing.login())
	
	# res = resize_all_image_in_folder_and_save_to_new_folder('C:/Work/NVK48/IFS/TBKK/MST', 'C:/Work/NVK48/IFS/TBKK/tet')
	# print(res)

	comparison_file_name_and_excel("C:/Work/NVK48/IFS/TBKK/EmployeeData/EmployeeFaceImage/TBKK", "C:/Work/NVK48/IFS/TBKK/EmployeeData/EmployeeForFace48.xlsx")

	print(shenxing.logout())