import socket
import sys
import re


#checks whether ipv4 address is valid or not.
def ipv4_validity(ip_addr):
	ip_octets = ip_addr.split('.')
	#ip_octets = sys.argv[1].split('.')
	#print ip_octets
	if (len(ip_octets) == 4) and (0 < int(ip_octets[0]) < 223) and (0 <= int(ip_octets[1]) < 255) and (0 <= int(ip_octets[2]) < 255) and (0 < int(ip_octets[3]) < 255) and (int(ip_octets[0]) != 169 or int(ip_octets[1]) != 254):		
		return ip_addr	
	else:
		print "ip address entered for server is invalid. Please try again."
		sys.exit()

#check whether ipv6 address syntax is valid or not.
def ipv6_validity(ip_addr):
	#a = '2000:4::6:7:2:3:4'

	if len(ip_addr.split(':')) > 8:
		print "Invalid IPv6 address.\nIPv6 address has more than 8 hextets."
		sys.exit()

	if len(ip_addr) == 3 and ((re.match('[0-9a-f]', ip_addr[0], re.I)) or (re.match('[0-9a-f]', ip_addr[1], re.I)) or (re.match('[g-z]', ip_addr[2], re.I))):
		print "IPv6 address is invalid. Please try again. You may be trying loopback address which is invalid."
		sys.exit()

	i = 0
	j = 0
	double_colon = 0
	ip_hex = []
	while i < len(ip_addr):
		if ip_addr[i] == ':' and ip_addr[i+1] == ':':		
			ip_hex.append(ip_addr[j:i])		
			i += 2
			j = i
			double_colon += 1
			if double_colon > 1:
				print "Invalid IPv6 address.\nIPv6 address cannot have more than one double colon."
				sys.exit()		
			continue
			
		elif ip_addr[i] == ':':
			ip_hex.append(ip_addr[j:i])		
			i += 1
			j = i	
			continue
		elif i == (len(ip_addr) - 1):	
			ip_hex.append(ip_addr[j:])
		i += 1	

	#print ip_hex


	if double_colon == 0 and len(ip_hex) != 8:
		print "IPv6 address is invalid. You need to have 8 hextets if you are not using a double colon."
		sys.exit()

	for element in ip_hex:	
		#print element	
		check = 0	
		if len(element) <= 4:
			check = hextet_check(element)
			if check == 0:
				print element, " is not hexadecimal"			
				sys.exit()


	if check == 1:
		return ip_addr

def hextet_check(hextet):	
	if re.match('[a-f0-9]{1,4}$', hextet, re.I):		
		return 1
	else:
		return 0

#if __name__ == "__main__":

if len(sys.argv) >= 4 and len(sys.argv) <= 6:
	#Assigns IPv4 or IPv6 address to host variable	
	if ':' in sys.argv[1]:
		if sys.argv[1] == '::1':
			host = '::1'
		else:
			host = ipv6_validity(sys.argv[1])
		
	else:
		host = ipv4_validity(sys.argv[1])
	
	#print host
	#Assigns port number to the port variable
	if (int(sys.argv[2]) >= 1024) and (sys.argv[2].isdigit()):  
		port = int(sys.argv[2])
	else:
		print "You may have entered one of the following. Please check.\n"
		print "1) Ports less than 1024 are system ports and cannot be defined by user. Please enter a port greater than or equal to 1024\n"
		print "2) Enter a number. You may have entered special characters or letters."
		sys.exit()
	#print port
	#Assigns request code to req_code variable
	if (sys.argv[3].isdigit()) and (1 <= int(sys.argv[3]) <= 6):	
		req_code = int(sys.argv[3])
	else:
		print "You may have entered a letter or a number greater than 6 for the request code. Please enter a number between 1 and 6."
		
		sys.exit()
	#print req_code
	#Assigns domain name which needs to be translated to the domain variable
	if len(sys.argv) > 4:	
		domain = sys.argv[4].lower()
		#print domain
		data_to_server = str(req_code) + " " + domain
	#Assigns ip address of the domain name that needs to stored in the domain-ip file in domain_ip variable	
	if len(sys.argv) == 6 and req_code == 2:
		if ':' in sys.argv[5]:
			domain_ip = ipv6_validity(sys.argv[5])
		else:
			domain_ip = ipv4_validity(sys.argv[5])
		data_to_server = data_to_server + " " + domain_ip
	
	#print host, port, req_code, domain
	#socket created
	if ':' in host:
		sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
	else:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
	sock.connect((host, port))								#Initiated TCP connection
	if (req_code == 4 or req_code == 5) and len(sys.argv) == 4:	
		sock.send(str(req_code))							#send data to server
	elif req_code == 1 or req_code == 2 or req_code == 3 or req_code == 6:
		sock.send(data_to_server)							#send data to server
	else:
		print "Wrong number of command line parameters. Please run 'python (client script file) (server IP) (server port) (req_code) (optional - domain name) (optional - domain IP)"
		sock.close()		
		sys.exit()								
	result = sock.recv(4096)								#receive data from server
	print result
	sock.close()										#socket closed
else:
	print "Wrong number of command line parameters. Please run 'python (client script file) (server IP) (server port) (req_code) (optional - domain name) (optional - domain IP)"
	sys.exit()

