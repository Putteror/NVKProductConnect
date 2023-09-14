from shenxing_7 import *

shenxing = Shenxing(hostAddress='http://192.168.33.108', username='admin', password='nvk12345')

print(shenxing.login())

print(shenxing.get_person_list())
# 
# print(shenxing.get_device_operation())
# print(shenxing.set_device_operation(key="1234123412341234"))

print(shenxing.logout())

# print(aes_encryption("0123456789012345","test"))