from Face48 import *

face48 = Face48(hostAddress='https://dev.face48.com/', username='iyo@nvk.co.th', password='P@ssw0rd!234')

face48.login()
# print(face48.get_guard_tour_schedule())
print(face48.create_guard_tour_schedule())
# print(face48.update_guard_tour_schedule_by_id("64e462f0a665b3d1b39876cc"))
# print(face48.delete_guard_tour_schedule_by_id("64e492098198f570049d6af2"))