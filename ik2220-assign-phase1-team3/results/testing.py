from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import sys
from time import sleep 
import os

PHASE1_LOG = '../results/phase_1_report'

class Testing(object):

	def __init__(self, net):
		self.net = net
		self.h1 = self.net.get('h1')
		self.h2 = self.net.get('h2')
		self.h3 = self.net.get('h3')
		self.h4 = self.net.get('h4')
		self.ds1 = self.net.get('h5')
		self.ds2 = self.net.get('h6')
		self.ds3 = self.net.get('h7')
		self.ws1 = self.net.get('h8')
		self.ws2 = self.net.get('h9')
		self.ws3 = self.net.get('h10')
		self.file = open('phase_1_report', 'w')



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
		if "Connection timed out" in test_message:
			return False
		else:
			return False

	def pingTest(self):
		ping_success = 0
		ping_total = 0
	
        	self.file.write("=================Ping Test===============\n")

		# H1 Ping H2
		result1 = self.h1.cmdPrint('ping -c 1 100.0.0.12')
		self.file.write('H1 -> H2 :'+result1+'\n')
		if self.parsePing(result1):
			self.file.write('H1 -> H2 : Success\n')
			ping_success = ping_success+1
			ping_total = ping_total+1
		else:
			self.file.write('H1 -> H2 : Failed\n')
			ping_total = ping_total+1

		# H1 Ping H3
        	result2 = self.h1.cmdPrint('ping -c 1 100.0.0.51')
       		self.file.write('H1 -> H3 :'+result2+'\n')
		if self.parsePing(result2):
			self.file.write('H1 -> H3 : Success\n')
			ping_success = ping_success+1
			ping_total = ping_total+1
        	else:
           		self.file.write('H1 -> H3 : Failed\n')
			ping_total = ping_total+1

		# H1 Ping DNS Server 1
		result3 = self.h1.cmdPrint('ping -c 1 100.0.0.20')
		self.file.write('H1 -> DNS Server 1 :'+result3+'\n')
		if self.parsePing(result3):
			self.file.write('H1 -> DNS Server 1 : Success\n')
			ping_success = ping_success+1
			ping_total = ping_total+1
		else:
			self.file.write('H1 -> DNS Server 1 : Failed\n')
			ping_total = ping_total+1
		
		# H1 Ping Web Server 1
		result4 = self.h1.cmdPrint('ping -c 1 100.0.0.40')
		self.file.write('H1 -> Web Server 1 :'+result4+'\n')
		if self.parsePing(result4):
			self.file.write('H1 -> Web Server 1 : Success\n')
			ping_success = ping_success+1
			ping_total = ping_total+1
		else:
			self.file.write('H1 -> Web Server 1 : Failed\n')
			ping_total = ping_total+1
                
		# H3 Ping H4
		result5 = self.h3.cmdPrint('ping -c 1 100.0.0.52')
		self.file.write('H3 -> H4 :'+result5+'\n')
		if self.parsePing(result5):
			self.file.write('H3 -> H4 : Success\n')
			ping_success = ping_success+1
			ping_total = ping_total+1
		else:
			self.file.write('H3 -> H4 : Failed\n')
			ping_total = ping_total+1

		# H3 Ping H1
		result6 = self.h3.cmdPrint('ping -c 1 100.0.0.11')
		self.file.write('H3 -> H1 :'+result6+'\n')
		if self.parsePing(result6):
			self.file.write('H3 -> H1 : Success\n')
			ping_success = ping_success+1
			ping_total = ping_total+1
		else:
			self.file.write('H3 -> H1 : Failed\n')
			ping_total = ping_total+1

		# H3 Ping DNS Server 1
		result7 = self.h3.cmdPrint('ping -c 1 100.0.0.20')
		self.file.write('H3 -> DNS Server 1 :'+result7+'\n')
		if self.parsePing(result7):
            		self.file.write('H3 -> DNS Server 1 : Success\n')
			ping_success = ping_success+1
			ping_total = ping_total+1
        	else:
            		self.file.write('H3 -> DNS Server 1 : Failed\n')
			ping_total = ping_total+1
		
		# H3 Ping Web Server 1
        	result8 = self.h3.cmdPrint('ping -c 1 100.0.0.40')
        	self.file.write('H3 -> Web Server 1 :'+result8+'\n')
        	if self.parsePing(result8):
        		self.file.write('H3 -> Web Server 1 : Success\n')
        		ping_success = ping_success+1
			ping_total = ping_total+1
       		else:
			self.file.write('H3 -> Web Server 1 : Failed\n')
			ping_total = ping_total+1


		self.file.write("\n"+str(ping_total)+"ICMP packets sent, "+str(ping_success)+" was success.\n")


	def dnsTest(self):

		dns_success = 0
		dns_total = 0
        	self.ds1.cmdPrint('python ds1.py &')
		self.ds2.cmdPrint('python ds2.py &')
		self.ds3.cmdPrint('python ds3.py &')
		
		sleep(2)

		self.file.write('=================DNS Test===============\n')

		# H1 Dig ws1.com to DNS Server 1 port 53
		result1 = self.h1.cmdPrint('dig -p 53 @100.0.0.20 ws1.com')
		self.file.write('h1 dig ds1 to port 53:\n'+result1+'\n')
		if self.parseDNS(result1):
			self.file.write("Success\n")
			dns_success = dns_success+1
			dns_total = dns_total+1
		else:
			self.file.write("Failed\n")
			dns_total = dns_total+1
		
		# H1 Dig ws1.com to DNS Server 1 port 60
		result2 = self.h1.cmdPrint('dig -p 60 @100.0.0.20 ws1.com')
		self.file.write('h1 dig ds1 to port 60:\n'+result2+'\n')
		if self.parseDNS(result2):
			self.file.write("Success\n")
			dns_success = dns_success+1
			dns_total = dns_total+1
		else:
			self.file.write("Failed\n")
			dns_total = dns_total+1
                
		# H1 Dig ws1.com to DNS Server 1 port 100
		result3 = self.h1.cmdPrint('dig -p 100 @100.0.0.20 ws1.com')
		self.file.write('h1 dig ds1 to port 100:\n'+result3+'\n')
		if self.parseDNS(result3):
			self.file.write("Success\n")
			dns_success = dns_success+1
			dns_total = dns_total+1
		else:
			self.file.write("Failed\n")
			dns_total = dns_total+1
                
		# H3 Dig ws1.com to DNS Server 2 port 53
		result4 = self.h3.cmdPrint('dig -p 53 @100.0.0.21 ws2.com')
		self.file.write('h3 dig ds2 to port 53:\n'+result4+'\n')
		if self.parseDNS(result4):
			self.file.write("Success\n")
			dns_success = dns_success+1
			dns_total = dns_total+1
		else:
			self.file.write("Failed\n")
			dns_total = dns_total+1
                
		# H3 Dig ws1.com to DNS Server 2 port 60
		result5 = self.h3.cmdPrint('dig -p 60 @100.0.0.21 ws2.com')
		self.file.write('h3 dig ds2 to port 60:\n'+result5+'\n')
		if self.parseDNS(result5):
			self.file.write("Success\n")
			dns_success = dns_success+1
			dns_total = dns_total+1
		else:
			self.file.write("Failed\n")
			dns_total = dns_total+1
                
		# H3 Dig ws1.com to DNS Server 2 port 100
		result6 = self.h3.cmdPrint('dig -p 100 @100.0.0.21 ws2.com')
		self.file.write('h3 dig ds2 to port 100:\n'+result6+'\n')
		if self.parseDNS(result6):
			self.file.write("Success\n")
			dns_success = dns_success+1
			dns_total = dns_total+1
		else:
			self.file.write("Failed\n")
			dns_total = dns_total+1

		self.file.write("\n"+str(dns_total)+" DNS requests sent. "+ str(dns_success)+" was success\n")

	def tcpTest(self):
		
		tcp_success = 0
		tcp_total = 0

		self.file.write('=================TCP Test===============\n')
    
		self.ws1.cmdPrint('python -m SimpleHTTPServer 80 &')
		self.ws2.cmdPrint('python -m SimpleHTTPServer 80 &')
		self.ws3.cmdPrint('python -m SimpleHTTPServer 80 &')

		sleep(2)

		# H1 curl Web server 1 port 80
		result1 = self.h1.cmdPrint('curl 100.0.0.40:80')
		self.file.write('H1 -> Web Server1 Port 80:\n'+result1+'\n')
		if self.parseTCP(result1):
			self.file.write("Success\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n")
			tcp_total = tcp_total+1
	
		# H1 curl Web server 1 port 90
		result2 = self.h1.cmdPrint('curl 100.0.0.40:90')
		self.file.write('H1 -> Web Server1 Port 90:\n'+result2+'\n')
		if self.parseTCP(result2):
			self.file.write("Success\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n")
			tcp_total = tcp_total+1
                
		# H1 curl Web server 1 port 100
		result3 = self.h1.cmdPrint('curl 100.0.0.40:100')
		self.file.write('H1 -> Web Server1 Port 100:\n'+result3+'\n')
		if self.parseTCP(result3):
			self.file.write("Success\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n")
			tcp_total = tcp_total+1
                
		# H3 curl Web server2 port 80
		result4 = self.h3.cmdPrint('curl 100.0.0.41:80')
		self.file.write('H3 -> Web Server 2 Port 80:\n'+result4+'\n')
		if self.parseTCP(result4):
			self.file.write("Success\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n")
			tcp_total = tcp_total+1
                
		# H3 curl Web server 2 port 90
		result5 = self.h3.cmdPrint('curl 100.0.0.41:90')
		self.file.write('H3 -> Web Server 2 Port 90:\n'+result5+'\n')
		if self.parseTCP(result5):
			self.file.write("Success\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n")
			tcp_total = tcp_total+1
                
		# H3 curl Web server 2 port 100
		result6 = self.h3.cmdPrint('curl 100.0.0.41:100')
		self.file.write('H3 -> Web Server 2 Port 100:\n'+result6+'\n')
		if self.parseTCP(result6):
			self.file.write("Success\n")
			tcp_success = tcp_success+1
			tcp_total = tcp_total+1
		else:
			self.file.write("Failed\n")
			tcp_total = tcp_total+1

		self.file.write("\n"+str(tcp_total)+" TCP packets sent. "+str(tcp_success)+" was success\n")

	def run_tests(self):
		log = open(PHASE1_LOG, 'w+')
		self.pingTest()
		self.file.write("\n\n")
		self.dnsTest()
		self.file.write("\n\n")
		self.tcpTest()
		self.file.close()

