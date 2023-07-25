from face48 import Face48

face48 = Face48(hostAddress='http://192.168.33.56', username='admin', password='P@ssw0rd2023')
face48.login()

def get_all_history_log_id_list():

	get_history_log = face48.get_history_log_list()

	all_log_count = get_history_log['page']['count']

	get_all_history_log = face48.get_history_log_list(size=all_log_count)

	history_log_list = get_all_history_log['data']

	history_log_id_list = []

	for history_log in history_log_list :

		history_log_id_list.append(history_log['id'])

	return history_log_id_list

def delete_all_history_log():

	history_log_id_list = get_all_history_log_id_list()

	delete_history_log_response = face48.delete_history_logs_by_id(log_id_list=history_log_id_list)

	print(delete_history_log_response)





if __name__ == '__main__':
	delete_all_history_log()

