from fastapi import FastAPI, Request, HTTPException
from fastapi.requests import Request
from xml.etree import ElementTree as ET
import uvicorn
import socket
import time
from datetime import datetime
import xmltodict, json

app = FastAPI()

def convert_xml_to_json(xml_string):

    xml_dict = xmltodict.parse(xml_string)
    json_data = json.dumps(xml_dict, indent=4)

    return json_data

@app.post("/xml")
async def receive_xml(request: Request):
    try:
        xml_str = await request.body()

        response = convert_xml_to_json(xml_str)
        # root = ET.fromstring(xml_str)
        
        # # Printing the XML structure
        # print(ET.dump(root))

        print(response)

        
        return {"message": "XML received and printed successfully"}
    except ET.ParseError:
        raise HTTPException(status_code=400, detail="Invalid XML data")

@app.post("/")
async def get_data_from_tiktok(request: Request):

	data = await request.json()
	print("Scan!!!", datetime.now())
	return data

@app.post("/callback/api/event")
async def get_data_from_tiktok(request: Request):

	data = await request.json()
	print("alarm!!!", datetime.now())
	print(data)
	return data

if __name__ == '__main__':
	uvicorn.run("callback:app",host='192.168.33.54', port=5000)   
 