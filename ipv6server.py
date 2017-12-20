import socket
import sys
import time


def server_func(port, file_name, ip_protocol):
	port = int(port)
	"""
	time_gap = int(time_gap)
	last_req_time = 0
	"""
	#print port, file_name

	data_file = open(file_name, "a+")						#opens the file containing the domain-ip translation
	data_file.seek(0)
	
	#line = data_list.next()

	domain_list = data_file.readlines()						# reads lines from file and stores it in domain_list where each element in domain_list is a line of the file.
	file_dict = {}									# empty dictionary to store the segregated data from the file
	for index,domain_info in enumerate(domain_list):
		data_web = domain_info.split(" ")
		data_web[-1] = data_web[-1].replace('\n','')
		#print data_web
		file_dict[index+1] = data_web
	#print file_dict
	#sock.close()
	sock.bind((host,port))								# binds host and port to the socket
	sock.listen(5)									# socket is in listening state
	print "Socket is in listening state"	
	while True:
		conn, addr = sock.accept()						# socket is accepting connections
		data_from_client_temp = conn.recv(1024)					# data from client is stored in data_from_client variable
		if " " in data_from_client_temp:
			data_from_client = data_from_client_temp.split(" ")
			req_code = int(data_from_client[0])
		else:
			data_from_client = data_from_client_temp 		
			req_code = data_from_client
			req_code = int(req_code)			
		"""		
		curr_time = time.time()
		if (curr_time - last_req_time) < time_gap:	
			print "Enquiry had been made ", curr_time - last_req_time, " seconds ago. Please wait for ", time_gap - (curr_time - last_req_time), " seconds for another query. Time gap between requests must be atleast ", time_gap
			sys.exit()
		"""
		#print data_from_client
		if req_code == 6:
			PASSWORD = data_from_client[1]					# assigns password to password variable
		elif req_code == 1 or req_code == 2 or req_code == 3 :
			domain = data_from_client[1]					# assigns domain name to domain variable
		#print domain
		if len(data_from_client) == 3:
			domain_ip = data_from_client[2]
		if req_code == 1:
			list_ip = []
			for index, search_domain in file_dict.items():
				if search_domain[0] == domain:
					list_ip = search_domain[2:]										
					conn.send(str(list_ip))
					file_dict[index][1] = int(file_dict[index][1]) + 1
					break
				else:
					continue
			if list_ip == []:						
				try:	
					info_domain = [domain, 1]			
					tuple_info  = socket.getaddrinfo(domain, 80)
					#print tuple_info
					if ip_protocol == 'ipv4':
						for info in tuple_info:
							addr = info[4][0]
							if len(addr) < 16:					
								list_ip.append(addr)
								info_domain.append(addr)	
					elif ip_protocol == 'ipv6':
						for info in tuple_info:
							addr = info[4][0]
							if ':' in addr:					
								list_ip.append(addr)
								info_domain.append(addr)
						if list_ip == []:
							conn.send("This domain name does not have IPv6 addresses.")				
							continue
					conn.send(str(list_ip))
					file_dict[(len(file_dict.keys())+1)] = info_domain
				except socket.gaierror:
					conn.send("Server could not resolve the domain name. Please check your domain name again")			
					
		
		elif req_code == 2:
			check_add = 1	
			for search_domain in file_dict.items():
				if search_domain[0] == domain:
					conn.send("The record to be added already exists")
					check_add = 0
					break
			if check_add == 1:		
				file_dict[(len(file_dict.keys())+1)] = [domain, 1, domain_ip]
				conn.send("Record added")
			
		elif req_code == 3:
			check_del = 0
			for index, search_domain in file_dict.items():
					if search_domain[0] == domain:
						del file_dict[index]
						check_del = 1
						conn.send("Record Deleted")
						break
			if check_del == 0:
				conn.send("The record to be deleted does not exist")
		
		elif req_code == 4:
			max_record = 0
			for info_list in file_dict.values():
				no_of_records = int(info_list[1])
				if no_of_records >= max_record:
					max_record = no_of_records
			most_req = []
			for info_list in file_dict.values():
				if int(info_list[1]) == max_record:
					most_req.append(info_list)
			conn.send(str(most_req))
		elif req_code == 5:
			min_record = 9999
			for info_list in file_dict.values():
				no_of_records = int(info_list[1])
				if no_of_records < min_record:
					min_record = no_of_records
			least_req = []
			for info_list in file_dict.values():
				if int(info_list[1]) == min_record:
					least_req.append(info_list)
			conn.send(str(least_req))
			
		elif req_code == 6:
			if PASSWORD == 'shuttheserver':
				conn.close()
				print "Server is shutting down"
				#sock.close()
				data_file.seek(0)
				data_file.truncate()
				for info_list in file_dict.values():
					i = 0
					while i < len(info_list):
						data_file.write(str(info_list[i]))
						if i < (len(info_list) - 1):						
							data_file.write(" ")
						i += 1
					data_file.write("\n")
				data_file.close()
				break
			else:
				conn.send("Password entered is wrong. Please try again.")
			


if len(sys.argv) == 4:	
	#creates ipv4 socket
	if sys.argv[3] == 'ipv4' and sys.argv[2] == 'ipv4_list.txt':
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
		host = socket.getaddrinfo(socket.gethostname(), 80, socket.AF_INET)[0][4][0]
		file_name = sys.argv[2]
		#print host
	#creates  ipv6 socket
	elif sys.argv[3] == 'ipv6' and sys.argv[2] == 'ipv6_list.txt':
		sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
		host = socket.getaddrinfo(socket.gethostname(), 80, socket.AF_INET6)[0][4][0]
		file_name = sys.argv[2]
	else:
		print "You have entered wrong network protocol or file name. Please try again."
		sys.exit()
else:
	print "Number of command line parameters must be four. Please run 'python (server script file) (port number) (file name that stores dns data) (ip protocol)'"
	sys.exit()	

server_func(sys.argv[1], file_name, sys.argv[3])

