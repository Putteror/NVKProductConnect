import requests
import time
import hashlib

class Hongtu :

	def __init__(self, hostAddress, username, password):

		self.ctimestamp = int(time.time() * 1000)
		self.secretkey = "sdfajk3242324fa! djq7" 
		self.cappkey = "appkey1"
		self.cnonce = "1234344"

		self.hostAddress = hostAddress

	def csign(self, url, method, query, requestBody):

		requestBodyMD5 = hashlib.md5(requestBody.encode()).hexdigest()

		string_to_hash = f"{url}-{method}-{query}-{requestBodyMD5}-{self.secretkey}-{self.ctimestamp}-{self.cnonce}-{self.cappkey}"

		print(string_to_hash)

		signature = hashlib.md5(string_to_hash.encode()).hexdigest()

		return signature

	def get_person_list(self):

		path = "/api/person/list"
		url = self.hostAddress + path

		requestBody = {"pageNum":1, "pageSize":10}

		csign = self.csign(url, "POST", "", str(requestBody))
		print(csign)

		headers = {

			"ctimestamp" : str(self.ctimestamp),
			"cnonce" : self.cnonce,
			"cappkey" : self.cappkey,
			"csign" : csign,
			"Content-Type" : "application/json"
		}

		print(headers)

		resp_data = requests.get(url=url, headers=headers)

		return resp_data.text

if __name__ == '__main__':
	
	hongtu_object = Hongtu(hostAddress="http://192.168.21.110", username="admin", password="Megvii123")

	print(hongtu_object.get_person_list())






		
