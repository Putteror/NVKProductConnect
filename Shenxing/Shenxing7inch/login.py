#!/usr/bin/python
# -*- coding: utf-8 -*-
import hashlib
import requests
import json
import time

CHALLENGE_URL = '/api/auth/login/challenge'
LOGIN_URL = '/api/auth/login'
LOGOUT_URL = '/api/auth/logout'

def encrypt_string(hash_string):
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature
	
class Shenxing():

	def __init__(self, hostAddress, username, password):

		self.hostAddress = hostAddress
		self.username = username
		self.password = password
		self.sessionId = ''

	def challenge(self):

		api_url = self.hostAddress + CHALLENGE_URL + f'?username={self.username}'
		response = requests.get(url=api_url)

		return_data = response.json()

		return return_data
	

	def login(self):

		challenge = self.challenge()

		salt = str(challenge["salt"])
		cha = str(challenge["challenge"])
		session = str(challenge["session_id"])

		key = self.password + salt + cha 

		password_encrypt = encrypt_string(key)

		headers = {'Content-Type': 'application/json'}

		requestsBody = {
			"session_id": session,
			"username": self.username,
			"password": password_encrypt
		}

		api_url =  self.hostAddress + LOGIN_URL
		response = requests.post(url=api_url, json=requestsBody, headers=headers)

		return_data = response.json()

		self.sessionId = return_data['session_id']

		return return_data
		
	def logout(self):

		api_url = self.hostAddress + LOGOUT_URL
		headers = {"Cookie" : f'sessionID={self.sessionId}'}

		response = requests.get(url=api_url, headers=headers)

		return_data = response.text

		return return_data, self.sessionId

if __name__ == '__main__':

	shenxing = Shenxing(hostAddress='http://192.168.21.59', username='admin', password='')
	print(shenxing.login())