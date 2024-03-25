import requests
import base64
import uuid, hmac, hashlib
from datetime import datetime

def hikcentral_pro_auth(server_ip, app_key, app_secret, path):
	now = datetime.now()
	timestamp = str(int(now.timestamp()) *1000)
	date = now.strftime('%Y-%m-%d %H:%M:%S')
	nonce = str(uuid.uuid4())

	HEADERS = {
    'x-ca-key': app_key,
    'x-ca-timestamp': timestamp,
    'x-ca-signature': None,
    'Date': date,
    'x-ca-signature-headers': 'x-ca-key,x-ca-nonce,x-ca-timestamp',
    'x-ca-nonce': nonce,
    'Content-Type': 'application/json'
	}

	message =  f'POST\n*/*\napplication/json\n{date}\nx-ca-key:{app_key}\nx-ca-nonce:{nonce}\nx-ca-timestamp:{timestamp}\n'+ path
	dig = hmac.new(app_secret.encode(), msg=message.encode(), digestmod=hashlib.sha256).digest()
	data = base64.b64encode(dig).decode()
	HEADERS['x-ca-signature'] = data	

	return HEADERS

if __name__ == '__main__':
	
	headers = hikcentral_pro_auth(server_ip="192.168.26.250:", app_key="22377924", app_secret="d8hKDkAHjYAA1GRxmtWj", path="/artemis/api/resource/v1/alarmInput/advance/alarmInputList")
	url = "https://192.168.26.250/artemis/api/resource/v1/alarmDevice/advance/alarmDeviceList"

	body = {

	    "pageNo": 1,
	    "pageSize": 10

	    }

	alarm_device_resp = requests.post(url, headers=headers, json=body, verify=False, timeout=7)
	alarm_resp = alarm_device_resp.text
	print(alarm_resp)
