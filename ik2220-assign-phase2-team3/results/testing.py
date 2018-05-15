from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.node import OVSSwitch
import sys
import time 
import os

PHASE2_LOG = '../results/phase_2_report'

class Testing(object):

	def __init__(self, net):
		self.net = net
		self.h1 = self.net.get('h1')
		self.h2 = self.net.get('h2')
		self.h3 = self.net.get('h3')
		self.h4 = self.net.get('h4')
		self.ds1 = self.net.get('ds1')
		self.ds2 = self.net.get('ds2')
		self.ds3 = self.net.get('ds3')
		self.ws1 = self.net.get('ws1')
		self.ws2 = self.net.get('ws2')
		self.ws3 = self.net.get('ws3')
		self.insp = self.net.get('insp')
		self.file = open('phase_2_report', 'w')



	def parsePing(self, test_message):
		"Parse"
		if 'Destination Host Unreachable' in test_message:
			return False
		if 'Network is unreachable' in test_message:
			return False
		if '100% packet loss' in test_message:		
			return False
		if '0% packet loss' in test_message:
			return True
		else:
			return True 

	def parseDNS(self, test_message):
		if "connection timed out" in test_message:
			return False
		else:
			return True

	def parseTCP(self, test_message):
		if "<html>" in test_message:
			return True
		if "Error code 501" in test_message:
			return True
		if "Operation timed out" in test_message:
			return False
		if "No route to host":
			return False	
		else:
			return False

	def pingTest(self):
		ping_success = 0
		ping_total = 0
	
		self.file.write("======================Ping Test=====================\n")

		# H1 Ping H2
		result1 = self.h1.cmdPrint('ping -c 1 100.0.0.11')
		self.file.write('Case 1: H1 -> H2 :'+result1)
		if self.parsePing(result1):
			self.file.write('Success\n\n')
			ping_success = ping_success+1
			ping_total = ping_total+1
		else:
			self.file.write('Failed\n\n')
			ping_total = ping_total+1

		# H1 Ping H3
		result2 = self.h1.cmdPrint('ping -c 1 100.0.0.50')
		self.file.write('Case 2: H1 -> H3 :'+result2)
		if self.parsePing(result2):
			self.file.write('Success\n\n')
			ping_success = ping_success+1
			ping_total = ping_total+1
		else:
			self.file.write('Failed\n\n')
			ping_total = ping_total+1

		# H1 Ping H4
		result3 = self.h1.cmdPrint('ping -c 1 100.0.0.51')
		self.file.write('Case 3: H1 -> H4 :'+result3)
		if self.parsePing(result3):
			self.file.write('Success\n\n')
			ping_success = ping_success+1
			ping_total = ping_total+1
		else:
			self.file.write('Failed\n\n')
			ping_total = ping_total+1

		# H1 Ping Load Balancer 1
		result4 = self.h1.cmdPrint('ping -c 1 100.0.0.25')
		self.file.write('Case 4: H1 -> Load Balancer 1 :'+result4)
		if self.parsePing(result4):
			self.file.write('Success\n\n')
			ping_success = ping_success+1
			ping_total = ping_total+1
		else:
			self.file.write('Failed\n\n')
			ping_total = ping_total+1

		# H1 Ping Load Balancer 2
		result5 = self.h1.cmdPrint('ping -c 1 100.0.0.45')
		self.file.write('H1 -> Load Balancer 2 :'+result5)
		if self.parsePing(result5):
			self.file.write('Success\n\n')
			ping_success = ping_success+1
			ping_total = ping_total+1
		else:
			self.file.write('Failed\n\n')
			ping_total = ping_total+1
		
		# H1 Ping Web Server 1
		result6 = self.h1.cmdPrint('ping -c 1 100.0.0.40')
		self.file.write('Case 6: H1 -> Web Server 1 :'+result6)
		if self.parsePing(result6):
			self.file.write('Success\n\n')
			ping_success = ping_success+1
			ping_total = ping_total+1
		else:
			self.file.write('Failed\n\n')
			ping_total = ping_total+1
        
        # H1 Ping DNS Server 1
		result7 = self.h1.cmdPrint('ping -c 1 100.0.0.20')
		self.file.write('Case 7: H1 -> DNS Server 1 :'+result7)
		if self.parsePing(result7):
			self.file.write('Success\n\n')
			ping_success = ping_success+1
			ping_total = ping_total+1
		else:
			self.file.write('Failed\n\n')
			ping_total = ping_total+1

		# H3 Ping H4
		result8 = self.h3.cmdPrint('ping -c 1 100.0.0.52')
		self.file.write('Case 8: H3 -> H4 :'+result8)
		if self.parsePing(result8):
			self.file.write(' Success\n\n')
			ping_success = ping_success+1
			ping_total = ping_total+1
		else:
			self.file.write('Failed\n\n')
			ping_total = ping_total+1

		# H2 Ping H3
		result9 = self.h2.cmdPrint('ping -c 1 100.0.0.50')
		self.file.write('Case 9: H2 -> H3 :'+result9)
		if self.parsePing(result9):
			self.file.write('Success\n\n')
			ping_success = ping_success+1
			ping_total = ping_total+1
		else:
			self.file.write('Failed\n\n')
			ping_total = ping_total+1

		# H2 Ping H4
		result10 = self.h2.cmdPrint('ping -c 1 100.0.0.51')
		self.file.write('Case 10: H2 -> H4 :'+result10)
		if self.parsePing(result10):
			self.file.write('Success\n\n')
			ping_success = ping_success+1
			ping_total = ping_total+1
		else:
			self.file.write('Failed\n\n')
			ping_total = ping_total+1

		# H2 Ping Load Balancer 1
		result11 = self.h2.cmdPrint('ping -c 1 100.0.0.25')
		self.file.write('Case 11: H2 -> Load Balancer 1 :'+result11)
		if self.parsePing(result11):
			self.file.write(' Success\n\n')
			ping_success = ping_success+1
			ping_total = ping_total+1
		else:
			self.file.write('Failed\n\n')
			ping_total = ping_total+1

		# H2 Ping Load Balancer 2
		result12 = self.h2.cmdPrint('ping -c 1 100.0.0.45')
		self.file.write('Case 12: H2 -> Load Balancer 2 :'+result12)
		if self.parsePing(result12):
			self.file.write('Success\n\n')
			ping_success = ping_success+1
			ping_total = ping_total+1
		else:
			self.file.write('Failed\n\n')
			ping_total = ping_total+1

		# H2 Ping DNS Server 1
		result13 = self.h2.cmdPrint('ping -c 1 100.0.0.20')
		self.file.write('Case 13: H2 -> DNS Server 1 :'+result13)
		if self.parsePing(result13):
			self.file.write('Success\n\n')
			ping_success = ping_success+1
			ping_total = ping_total+1
		else:
			self.file.write('Failed\n\n')
			ping_total = ping_total+1

		# H2 Ping Web Server 1
		result14 = self.h2.cmdPrint('ping -c 1 100.0.0.40')
		self.file.write('Case 14: H2 -> Web Server 1 :'+result14)
		if self.parsePing(result14):
			self.file.write('Success\n\n')
			ping_success = ping_success+1
			ping_total = ping_total+1
		else:
			self.file.write('Failed\n\n')
			ping_total = ping_total+1

		# H3 Ping H1
		result15 = self.h3.cmdPrint('ping -c 1 100.0.0.10')
		self.file.write('Case 15: H3 -> H1 :'+result15)
		if self.parsePing(result15):
			self.file.write('Success\n\n')
			ping_success = ping_success+1
			ping_total = ping_total+1
		else:
			self.file.write('Failed\n\n')
			ping_total = ping_total+1

		# H3 Ping H2
		result16 = self.h3.cmdPrint('ping -c 1 100.0.0.11')
		self.file.write('Case 16: H3 -> H2 :'+result16)
		if self.parsePing(result16):
			self.file.write('Success\n\n')
			ping_success = ping_success+1
			ping_total = ping_total+1
		else:
			self.file.write('Failed\n\n')
			ping_total = ping_total+1

		# H3 Ping Load Balancer 1
		result17 = self.h3.cmdPrint('ping -c 1 100.0.0.25')
		self.file.write('Case 17: H3 -> Load Balancer 1 :'+result17)
		if self.parsePing(result17):
			self.file.write('Success\n\n')
			ping_success = ping_success+1
			ping_total = ping_total+1
		else:
			self.file.write('Failed\n\n')
			ping_total = ping_total+1

		# H3 Ping Load Balancer 2
		result18 = self.h3.cmdPrint('ping -c 1 100.0.0.45')
		self.file.write('Case 18: H3 -> Load Balancer :'+result18)
		if self.parsePing(result18):
			self.file.write('Success\n\n')
			ping_success = ping_success+1
			ping_total = ping_total+1
		else:
			self.file.write('Failed\n\n')
			ping_total = ping_total+1

		# H3 Ping DNS Server 1
		result19 = self.h3.cmdPrint('ping -c 1 100.0.0.20')
		self.file.write('Case 19: H3 -> DNS Server 1 :'+result19)
		if self.parsePing(result19):
			self.file.write('Success\n\n')
			ping_success = ping_success+1
			ping_total = ping_total+1
		else:
			self.file.write(' Failed\n\n')
			ping_total = ping_total+1
		
		# H3 Ping Web Server 1
		result20 = self.h3.cmdPrint('ping -c 1 100.0.0.40')
		self.file.write('Case 20: H3 -> Web Server 1 :'+result20)
		if self.parsePing(result20):
			self.file.write('Success\n\n')
			ping_success = ping_success+1
			ping_total = ping_total+1       		
		else:
			self.file.write('Failed\n\n')
			ping_total = ping_total+1

		
		print("\nICMP Ping tests finished!\n Conclusion: "+str(ping_total)+" ICMP packets sent in total, "+str(ping_success)+" was success.\n")
		self.file.write("\nICMP Ping tests finished!\nConclusion: "+str(ping_total)+"ICMP packets sent in total, "+str(ping_success)+" was success. \nSuccess rate is "+str(ping_success)+"/"+str(ping_total)+"\n")


	def dnsTest(self):

		dns_success = 0
		dns_total = 0
		self.ds1.cmdPrint('python ../topology/ds1.py &')
		self.ds2.cmdPrint('python ../topology/ds2.py &')
		self.ds3.cmdPrint('python ../topology/ds3.py &')
		
		time.sleep(5)

		self.file.write('=======================DNS Test=======================\n')

		# H1 Dig team3.com to Load Balancer 1 port 53
		result1 = self.h1.cmdPrint('dig -p 53 @100.0.0.25 team3.com')
		self.file.write('Case 1: H1 dig Load Balancer 1 to port 53:\n'+result1)
		if self.parseDNS(result1):
			self.file.write("Success\n\n")
			dns_success = dns_success+1
			dns_total = dns_total+1
		else:
			self.file.write("Failed\n\n")
			dns_total = dns_total+1
		
		# H1 Dig team3.com to Load Balancer 1 port 60
		result2 = self.h1.cmdPrint('dig -p 60 @100.0.0.25 team3.com')
		self.file.write('Case 2: H1 dig Load Balancer 1 to port 60:\n'+result2)
		if self.parseDNS(result2):
			self.file.write("Success\n\n")
			dns_success = dns_success+1
			dns_total = dns_total+1
		else:
			self.file.write("Failed\n\n")
			dns_total = dns_total+1
                
		# H1 Dig team3.com to Load Balancer 1 port 100
		result3 = self.h1.cmdPrint('dig -p 100 @100.0.0.25 team3.com')
		self.file.write('Case 3: H1 dig Load Balancer 1 to port 100:\n'+result3)
		if self.parseDNS(result3):
			self.file.write("Success\n\n")
			dns_success = dns_success+1
			dns_total = dns_total+1
		else:
			self.file.write("Failed\n\n")
			dns_total = dns_total+1
		
		# H1 Dig team3.com to DNS Server 1 Actual IP port 53
		result4 = self.h1.cmdPrint('dig -p 53 @100.0.0.20 team3.com')
		self.file.write('Case 4: H1 dig DNS Server 1 Actual IP to port 53:\n'+result4)
		if self.parseDNS(result4):
			self.file.write("Success\n\n")
			dns_success = dns_success+1
			dns_total = dns_total+1
		else:
			self.file.write("Failed\n\n")
			dns_total = dns_total+1
		
		# H1 Dig team3.com to DNS Server 2 Actual IP port 53
		result5 = self.h1.cmdPrint('dig -p 53 @100.0.0.21 team3.com')
		self.file.write('Case 1: H1 dig DNS Server 2 Actual IP to port 53:\n'+result5)
		if self.parseDNS(result5):
			self.file.write("Success\n\n")
			dns_success = dns_success+1
			dns_total = dns_total+1
		else:
			self.file.write("Failed\n\n")
			dns_total = dns_total+1
		
		# H1 Dig team3.com to DNS Server 3 Actual IP port 53
		result6 = self.h1.cmdPrint('dig -p 53 @100.0.0.22 team3.com')
		self.file.write('Case 6: H1 dig DNS Server 3 Actual IP to port 53:\n'+result6)
		if self.parseDNS(result6):
			self.file.write("Success\n\n")
			dns_success = dns_success+1
			dns_total = dns_total+1
		else:
			self.file.write("Failed\n\n")
			dns_total = dns_total+1
                
		# H3 Dig team3.com to Load Balancer 1 port 53
		result7 = self.h3.cmdPrint('dig -p 53 @100.0.0.25 team3.com')
		self.file.write('Case 7: H3 dig Load Balancer 1 to port 53:\n'+result7)
		if self.parseDNS(result7):
			self.file.write("Success\n\n")
			dns_success = dns_success+1
			dns_total = dns_total+1
		else:
			self.file.write("Failed\n\n")
			dns_total = dns_total+1
                
		# H3 Dig team3.com to Load Balancer 1 port 60
		result8 = self.h3.cmdPrint('dig -p 60 @100.0.0.25 team3.com')
		self.file.write('Case 8: H3 dig Load Balancer 1 to port 60:\n'+result8)
		if self.parseDNS(result8):
			self.file.write("Success\n\n")
			dns_success = dns_success+1
			dns_total = dns_total+1
		else:
			self.file.write("Failed\n\n")
			dns_total = dns_total+1
                
		# H3 Dig team3.com to Load Balancer 1 port 100
		result9 = self.h3.cmdPrint('dig -p 100 @100.0.0.25 team3.com')
		self.file.write('Case 9: H3 dig Load Balancer 1 to port 100:\n'+result9)
		if self.parseDNS(result9):
			self.file.write("Success\n\n")
			dns_success = dns_success+1
			dns_total = dns_total+1
		else:
			self.file.write("Failed\n\n")
			dns_total = dns_total+1

		# H3 Dig team3.com to DNS Server 1 actual IP port 53
		result10 = self.h3.cmdPrint('dig -p 53 @100.0.0.20 team3.com')
		self.file.write('Case 10: H3 dig Load Balancer 1 to port 53:\n'+result10)
		if self.parseDNS(result10):
			self.file.write("Success\n\n")
			dns_success = dns_success+1
			dns_total = dns_total+1
		else:
			self.file.write("Failed\n\n")
			dns_total = dns_total+1

		# H3 Dig team3.com to DNS Server 2 actual IP port 53
		result11 = self.h3.cmdPrint('dig -p 53 @100.0.0.21 team3.com')
		self.file.write('Case 11: H3 dig DNS Server 2 actual IP to port 53:\n'+result11)
		if self.parseDNS(result11):
			self.file.write("Success\n\n")
			dns_success = dns_success+1
			dns_total = dns_total+1
		else:
			self.file.write("Failed\n\n")
			dns_total = dns_total+1

		# H3 Dig team3.com to DNS Server 3 actual IP port 53
		result12 = self.h3.cmdPrint('dig -p 53 @100.0.0.22 team3.com')
		self.file.write('Case 12: H3 dig DNS Server 3 actual IP to port 53:\n'+result12)
		if self.parseDNS(result12):
			self.file.write("Success\n\n")
			dns_success = dns_success+1
			dns_total = dns_total+1
		else:
			self.file.write("Failed\n\n")
			dns_total = dns_total+1

		print("\nDNS Tests finished!\n Conclusion: "+str(dns_total)+" DNS requests sent. "+ str(dns_success)+" was success\n")
		self.file.write("\nDNS Tests finished!\nConclusion: "+str(dns_total)+" DNS requests sent. "+ str(dns_success)+" was success\n")
		self.file.write("The success rate is "+str(dns_success)+"/"+str(dns_total)+".\n")
		self.ds1.cmdPrint('kill %python')
		self.ds2.cmdPrint('kill %python')
		self.ds3.cmdPrint('kill %python')

	def tcpTest(self):
		
		tcp_success = 0
		tcp_total = 0

		self.file.write('====================TCP Test====================\n')
		self.file.write('This part will test the function of IDS and Load Balancer 2.\n')
    
		self.ws1.cmdPrint('python -m SimpleHTTPServer 80 &')
		self.ws2.cmdPrint('python -m SimpleHTTPServer 80 &')
		self.ws3.cmdPrint('python -m SimpleHTTPServer 80 &')
		self.insp.cmdPrint('tcpdump -w insp.pcap &')

		time.sleep(5)

		# H1 curl Load Balancer 2 Web port 80 method POST
		result1 = self.h1.cmdPrint('curl --max-time 20 -X POST -d "user=admin&passwd=12345678" http://100.0.0.45:80')
		self.file.write('Case 1: H1 -> Load Balancer 2 Web Port 80 method POST:\n\n'+result1+'\n')
		if self.parseTCP(result1):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1
			
		
		# H1 curl Load Balancer 2 Web Port 80 method PUT
		result2 = self.h1.cmdPrint('curl --max-time 20 -X PUT -d "user=admin&passwd=12345678" http://100.0.0.45:80')
		self.file.write('Case 2: H1 -> Load Balancer 2 Web Port 80 method PUT:\n'+result2+'\n\n')
		if self.parseTCP(result2):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1
		
		# H3 curl Load Balancer 2 Web port 80 method POST
		result3 = self.h3.cmdPrint('curl --max-time 20 -X POST -d "user=admin&passwd=12345678" http://100.0.0.45:80')
		self.file.write('Case 3: H3 -> Load Balancer 2 Web Port 80 method POST:\n\n'+result3+'\n')
		if self.parseTCP(result3):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1

		# H3 curl Load Balancer 2 Web port 80 method PUT
		result4 = self.h3.cmdPrint('curl --max-time 20 -X PUT -d "user=admin&passwd=12345678" http://100.0.0.45:80')
		self.file.write('Case 4: H3 -> Load Balancer 2 Web Port 80 method PUT:\n\n'+result4+'\n')
		if self.parseTCP(result4):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1

	
		# H1 curl Load Balancer 2 Web port 90 method POST
		result5 = self.h1.cmdPrint('curl --max-time 20 -X POST -d "user=admin&passwd=12345678" http://100.0.0.45:90')
		self.file.write('Case 5: H1 -> Load Balancer 2 Web Port 90 method POST:\n'+result5+'\n\n')
		if self.parseTCP(result5):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1
                
		# H1 curl Load Balancer 2 Web port 100 method POST
		result6 = self.h1.cmdPrint('curl --max-time 20 -X POST -d "user=admin&passwd=12345678" http://100.0.0.45:100')
		self.file.write('Case 6: H1 -> Load Balancer 2 Web Port 100 method POST:\n'+result6+'\n\n')
		if self.parseTCP(result6):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1

		# H1 curl Web Server 1 Actual IP Web port 80 method POST
		result7 = self.h1.cmdPrint('curl --max-time 20 -X POST -d "user=admin&passwd=12345678" http://100.0.0.40:80')
		self.file.write('Case 7: H1 -> Web Port 80 method POST:\n\n'+result7+'\n')
		if self.parseTCP(result7):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1

		# H1 curl Web Server 2 Actual IP Web port 80 method POST
		result8 = self.h1.cmdPrint('curl --max-time 20 -X POST -d "user=admin&passwd=12345678" http://100.0.0.41:80')
		self.file.write('Case 8: H1 -> Web Server 2 Actual IP Web Port 80 method POST:\n\n'+result8+'\n')
		if self.parseTCP(result8):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1

		# H1 curl Web Server 3 Actual IP Web port 80 method POST
		result9 = self.h1.cmdPrint('curl --max-time 20 -X POST -d "user=admin&passwd=12345678" http://100.0.0.42:80')
		self.file.write('Case 9: H1 -> Web Server 3 Actual IP Web Port 80 method POST:\n\n'+result9+'\n')
		if self.parseTCP(result9):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1

		# H1 curl Load Balancer 2 Web port 80 method GET
		result10 = self.h1.cmdPrint('curl --max-time 20 http://100.0.0.45:80')
		self.file.write('Case 10: H1 -> Load Balancer 2 Web Port 80 method GET:\n'+result10+'\n\n')
		if self.parseTCP(result10):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1

		# H1 curl Load Balancer 2 Web port 80 method HEAD
		result11 = self.h1.cmdPrint('curl --max-time 20 -X HEAD http://100.0.0.45:80')
		self.file.write('Case 11: H1 -> Load Balancer 2 Web Port 80 method HEAD:\n'+result11+'\n\n')
		if self.parseTCP(result11):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1

		# H1 curl Load Balancer 2 Web Port 80 method OPTIONS
		result12 = self.h1.cmdPrint('curl --max-time 20 -X OPTIONS http://100.0.0.45:80')
		self.file.write('Case 12: H1 -> Load Balancer 2 Web Port 80 method OPTIONS:\n'+result12+'\n\n')
		if self.parseTCP(result12):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1

		# H1 curl Load Balancer 2 Web Port 80 method TRACE
		result13 = self.h1.cmdPrint('curl --max-time 20 -X TRACE http://100.0.0.45:80')
		self.file.write('Case 13: H1 -> Load Balancer 2 Web Port 80 method TRACE:\n'+result13+'\n\n')
		if self.parseTCP(result13):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1

	
		# H1 curl Load Balancer 2 Web Port 80 method DELETE
		result14 = self.h1.cmdPrint('curl --max-time 20 -X DELETE http://100.0.0.45:80')
		self.file.write('Case 14: H1 -> Load Balancer 2 Web Port 80 method DELETE:\n'+result14+'\n\n')
		if self.parseTCP(result14):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1

		# H1 curl Load Balancer 2 Web Port 80 method CONNECT
		result15 = self.h1.cmdPrint('curl --max-time 20 -X CONNECT http://100.0.0.45:80')
		self.file.write('Case 15: H1 -> Load Balancer 2 Web Port 80 method CONNECT:\n'+result15+'\n\n')
		if self.parseTCP(result15):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1

		# H1 curl Load Balancer 2 Web Port 80 method PUT SQL cat /var/log/
		result16 = self.h1.cmdPrint('curl --max-time 20 -X PUT -d "cat /var/log/" http://100.0.0.45:80')
		self.file.write('Case 16: H1 -> Load Balancer 2 Web Port 80 method PUT SQL cat /var/log/:\n'+result16+'\n\n')
		if self.parseTCP(result16):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1

		# H1 curl Load Balancer 2 Web Port 80 method PUT SQL cat /etc/passwd
		result17 = self.h1.cmdPrint('curl --max-time 20 -X PUT -d "cat /etc/passwd" http://100.0.0.45:80')
		self.file.write('Case 17: H1 -> Load Balancer 2 Web Port 80 method PUT SQL cat /etc/passwd:\n'+result17+'\n\n')
		if self.parseTCP(result17):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1

		# H1 curl Load Balancer 2 Web Port 80 method PUT SQL INSERT
		result18 = self.h1.cmdPrint('curl --max-time 20 -X PUT -d "INSERT" http://100.0.0.45:80')
		self.file.write('Case 18: H1 -> Load Balancer 2 Web Port 80 method PUT SQL INSERT:\n'+result18+'\n\n')
		if self.parseTCP(result18):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1

		# H1 curl Load Balancer 2 Web Port 80 method PUT SQL UPDATE
		result19 = self.h1.cmdPrint('curl --max-time 20 -X PUT -d "UPDATE" http://100.0.0.45:80')
		self.file.write('Case 19: H1 -> Load Balancer 2 Web Port 80 method PUT SQL UPDATE:\n'+result19+'\n\n')
		if self.parseTCP(result19):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1

		# H1 curl Load Balancer 2 Web Port 80 method PUT SQL DELETE
		result20 = self.h1.cmdPrint('curl --max-time 20 -X PUT -d "DELETE" http://100.0.0.45:80')
		self.file.write('Case 20: H1 -> Load Balancer 2 Web Port 80 method PUT SQL DELETE:\n'+result20+'\n\n')
		if self.parseTCP(result20):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1

		
                
		# H3 curl Load Balancer 2 Web port 90 method POST
		result21 = self.h3.cmdPrint('curl --max-time 20 -X POST -d "user=admin&passwd=12345678" http://100.0.0.45:90')
		self.file.write('Case 21: H3 -> Load Balancer 2 Web Port 80 method POST:\n\n'+result21+'\n')
		if self.parseTCP(result21):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1
                
		# H3 curl Load Balancer 2 Web port 100 method POST
		result22 = self.h3.cmdPrint('curl --max-time 20 -X POST -d "user=admin&passwd=12345678" http://100.0.0.45:100')
		self.file.write('Case 22: H1 -> Load Balancer 2 Web Port 100 method POST:\n\n'+result22+'\n')
		if self.parseTCP(result22):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1

		# H3 curl Web Server 1 Actual IP Web port 80 method POST
		result23 = self.h3.cmdPrint('curl --max-time 20 -X POST -d "user=admin&passwd=12345678" http://100.0.0.40:80')
		self.file.write('Case 23: H3 -> Web Server Actual IP Web Port 80 method POST:\n\n'+result23+'\n')
		if self.parseTCP(result23):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1
		
		# H3 curl Web Server 2 Actual IP Web port 80 method POST
		result24 = self.h3.cmdPrint('curl --max-time 20 -X POST -d "user=admin&passwd=12345678" http://100.0.0.41:80')
		self.file.write('Case 24: H3 -> Web Server 2 Actual IP Web Port 80 method POST:\n\n'+result24+'\n')
		if self.parseTCP(result24):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1
		
		# H3 curl Web Server 3 Actual IP Web port 80 method POST
		result25 = self.h3.cmdPrint('curl --max-time 20 -X POST -d "user=admin&passwd=12345678" http://100.0.0.42:80')
		self.file.write('Case 25: H3 -> Load Balancer 2 Web Port 80 method POST:\n\n'+result25+'\n')
		if self.parseTCP(result25):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1

		# H3 curl Load Balancer 2 Web port 80 method GET
		result26 = self.h3.cmdPrint('curl --max-time 20 http://100.0.0.45:80')
		self.file.write('Case 26: H3 -> Load Balancer 2 Web Port 80 method GET:\n\n'+result26+'\n')
		if self.parseTCP(result26):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1

		# H3 curl Load Balancer 2 Web port 80 method HEAD
		result27 = self.h3.cmdPrint('curl --max-time 20 -X HEAD http://100.0.0.45:80')
		self.file.write('Case 27: H3 -> Load Balancer 2 Web Port 80 method HEAD:\n\n'+result27+'\n')
		if self.parseTCP(result27):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1

		# H3 curl Load Balancer 2 Web port 80 method OPTIONS
		result28 = self.h3.cmdPrint('curl --max-time 20 -X OPTIONS http://100.0.0.45:80')
		self.file.write('Case 28: H3 -> Load Balancer 2 Web Port 80 method OPTIONS:\n\n'+result28+'\n')
		if self.parseTCP(result28):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1

		# H3 curl Load Balancer 2 Web port 80 method TRACE
		result29 = self.h3.cmdPrint('curl --max-time 20 -X TRACE http://100.0.0.45:80')
		self.file.write('Case 29: H3 -> Load Balancer 2 Web Port 80 method TRACE:\n\n'+result29+'\n')
		if self.parseTCP(result29):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1


		# H3 curl Load Balancer 2 Web port 80 method DELETE
		result30 = self.h3.cmdPrint('curl --max-time 20 -X DELETE http://100.0.0.45:80')
		self.file.write('Case 30: H3 -> Load Balancer 2 Web Port 80 method DELETE:\n\n'+result30+'\n')
		if self.parseTCP(result30):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1

		# H3 curl Load Balancer 2 Web port 80 method CONNECT
		result31 = self.h3.cmdPrint('curl --max-time 20 -X CONNECT http://100.0.0.45:80')
		self.file.write('Case 31: H3 -> Load Balancer 2 Web Port 80 method CONNECT:\n\n'+result31+'\n')
		if self.parseTCP(result31):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1

		# H3 curl Load Balancer 2 Web port 80 method PUT SQL cat /var/log/
		result32 = self.h3.cmdPrint('curl --max-time 20 -X PUT -d "cat /var/log/" http://100.0.0.45:80')
		self.file.write('Case 32: H3 -> Load Balancer 2 Web Port 80 method PUT SQL cat /var/log/:\n\n'+result32+'\n')
		if self.parseTCP(result32):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1

		# H3 curl Load Balancer 2 Web port 80 method PUT SQL cat /etc/passwd
		result33 = self.h3.cmdPrint('curl --max-time 20 -X PUT -d "cat /etc/passwd" http://100.0.0.45:80')
		self.file.write('Case 33: H3 -> Load Balancer 2 Web Port 80 method PUT SQL cat /etc/passwd:\n\n'+result33+'\n')
		if self.parseTCP(result33):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1

		# H3 curl Load Balancer 2 Web port 80 method PUT SQL INSERT
		result34 = self.h3.cmdPrint('curl --max-time 20 -X PUT -d "INSERT" http://100.0.0.45:80')
		self.file.write('Case 34: H3 -> Load Balancer 2 Web Port 80 method PUT SQL INSERT:\n\n'+result34+'\n')
		if self.parseTCP(result34):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1

		# H3 curl Load Balancer 2 Web port 80 method PUT SQL UPDATE
		result35 = self.h3.cmdPrint('curl --max-time 20 -X PUT -d "UPDATE" http://100.0.0.45:80')
		self.file.write('Case 35: H3 -> Load Balancer 2 Web Port 80 method PUT SQL UPDATE:\n\n'+result35+'\n')
		if self.parseTCP(result35):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1

		# H3 curl Load Balancer 2 Web port 80 method PUT SQL DELETE
		result36 = self.h3.cmdPrint('curl --max-time 20 -X PUT -d "DELETE" http://100.0.0.45:80')
		self.file.write('Case 36: H3 -> Load Balancer 2 Web Port 80 method PUT SQL DELETE:\n\n'+result36+'\n')
		if self.parseTCP(result36):
			self.file.write("Success\n\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n\n")
			tcp_total = tcp_total+1


		self.file.write("\n HTTP tests finished! \n Conclusion: "+str(tcp_total)+" HTTP packets sent. "+str(tcp_success)+" was success\n")
		self.file.write("The success rate is "+str(tcp_success)+"/"+str(tcp_total)+".\n")
		self.ws1.cmd('kill %python')
		self.ws2.cmd('kill %python')
		self.ws3.cmd('kill %python')
		self.insp.cmd('kill %python')

	def run_tests(self):
		log = open(PHASE2_LOG, 'w+')
		self.pingTest()
		self.file.write("\n\n")
		self.dnsTest()
		self.file.write("\n\n")
		self.tcpTest()
		self.file.write("================Auto tests finished=================")
		self.file.close()

