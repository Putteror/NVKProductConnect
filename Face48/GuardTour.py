from Face48 import *

face48 = Face48(hostAddress='https://dev.face48.com/', username='iyo@nvk.co.th', password='P@ssw0rd!234')

requestsBody = {

				"name" : "putter Guard",
				"personIds" : ["648ff6b342565c0f9584448d"],
				"locationId" : "63170f36d25cc4b49d938304",
				"isFixed" : False,
				"sunday" : True,
				"sundayTime" : ["18:00", "19:00"],
				"monday" : False,
				"tuesday" : False,
				"wednesday" : False,
				"thursday" : False,
				"friday" : False,
				"saturday" : False,
				"earlyMinutes" : 10,
				"lateMinutes" : 10
				
			}

face48.login()
print(face48.get_guard_tour_schedule())
# print(face48.create_guard_tour_schedule(requestsBody=requestsBody))
# print(face48.update_guard_tour_schedule_by_id("64e462f0a665b3d1b39876cc"))
# print(face48.delete_guard_tour_schedule_by_id("64e492098198f570049d6af2"))