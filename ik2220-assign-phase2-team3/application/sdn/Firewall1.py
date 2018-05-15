from pox.core import core
from pox.forwarding.l2_learning import LearningSwitch
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt

log = core.getLogger()

class LearningFireWall1 (LearningSwitch):
	def __init__ (self, connection):
		LearningSwitch.__init__(self, connection, False)
	#Handle packet in message form the switch to implement above algorithm.	
	def _handle_PacketIn (self, event):
		#This is the parsed packet data.
		packet = event.parsed
		if not packet.parsed:
			log.warning("Incomplete packet.")
			return
		
		#Drop the packet and optionally install a flow to continue dropping similar ones for a while
		#The drop function is same as l2_learning
		def drop (duration = None):
			if duration is not None:
				if not isinstance(duration, tuple):
					duration = (duration,duration)
				msg = of.ofp_flow_mod()
				msg.match = of.ofp_match.from_packet(packet)
				msg.idle_timeout = duration[0]
				msg.hard_timeout = duration[1]
				msg.buffer_id = event.ofp.buffer_id
				self.connection.send(msg)
			elif event.ofp.buffer_id is not None:
				msg = of.ofp_packet_out()
				msg.buffer_id = event.ofp.buffer_id
				msg.in_port = event.port
				self.connection.send(msg)

		# firewall in port 1 (from PbZ to DmZ)
		if event.port == 1:
			if packet.find("arp"):
				a = packet.find("arp")
				if a.opcode == a.REPLY or a.opcode == a.REQUEST:
					super(LearningFireWall1, self)._handle_PacketIn(event)
					return
			
			ip = packet.find('ipv4')
			if ip is not None:
				icmp = ip.find('icmp')
				if icmp is not None:
					dstIp = ip.dstip
					srcIp = ip.srcip
					if icmp.type == 8:
						if dstIp == '100.0.0.11' or dstIp== '100.0.0.10' or dstIp == '100.0.0.25' or dstIp == '100.0.0.45':
							super(LearningFireWall1, self)._handle_PacketIn(event)
							print("f1 p1: A request packet is transmitted from (%s) to (%s) by icmp protocol:Success." %(srcIp,dstIp))
							return
						else:
							log.debug("A request packet is transmitted from (%s) to (%s) by icmp protocol:DROP." %(srcIp, dstIp))
							drop()
							print("f1 p1:A request packet is transmitted from (%s) to (%s) by icmp protocol:drop." %(srcIp, dstIp))
							return
					elif icmp.type == 0:
						super(LearningFireWall1, self)._handle_PacketIn(event)
						print("f1 p1: A response packet is transmitted from (%s) to (%s) by icmp protocol:Success." %(srcIp, dstIp))
						return
				
					else:
							log.debug("A response packet is transmitted from (%s) to (%s) by icmp protocol:DROP." %(srcIp, dstIp))
							drop()
							print("f1 p1: A response packet is transmitted from (%s) to (%s) by icmp protocol:Success." %(srcIp, dstIp))
							return
				tcp = ip.find('tcp')
				if tcp is not None:
					print("f1 p1: A packet is transmitted by tcp protocol.")					
					log.debug("f1 p1: A packet is transmitted by tcp protocol.")
					srcIp = ip.srcip
					dstIp = ip.dstip
					dstPort = tcp.dstport
					print("f1 p1: IP: %s ===== port: %s" %(dstIp,dstPort))
					f = tcp.ACK
					print("The ACK flag is %s" %f)
					if f == False:
						if dstPort == 80:
							if dstIp == '100.0.0.40' or dstIp == '100.0.0.41' or dstIp == '100.0.0.42' or dstIp == '100.0.0.45':
								super(LearningFireWall1, self)._handle_PacketIn(event)
								print("f1 p1: A packet is transmitted from (%s) to (%s) port (%s) by tcp protocol:success." %(srcIp,dstIp,dstPort))
								log.debug("f1 p1: A packet is transmitted from (%s) to (%s) port (%s) by tcp protocol." %(srcIp,dstIp,dstPort))
								return
							else:
								log.debug("f1 p1: A packet is transmitted to (%s) port (%s) by tcp protocol:DROP." %(dstIp, dstPort))
								drop()
								print("f1 p1: A packet is transmitted to (%s) port (%s) by tcp protocol:drop." %(dstIp, dstPort))
								return

						else:
							print("f1 p1: A packet is transmitted to (%s) port (%s) by tcp protocol:DROP." %(dstIp, dstPort))
							log.debug("f1 p1: A packet is transmitted to (%s) port (%s) by tcp protocol:DROP." %(dstIp, dstPort))
							drop()
							return
					elif f == True:
						print("The ACK flag is (%s)" %f)
						super(LearningFireWall1, self)._handle_PacketIn(event)
						print("f1 p1: A ACK packet is transmitted to (%s) port (%s) by tcp protocol:success." %(dstIp,dstPort))
						return
					
					
			


				udp = ip.find('udp')
				if udp is not None:
					log.debug("f1 p1: A packet is transmitted by udp protocol.")
					dstIp = ip.dstip
					srcIp = ip.srcip
					dstPort = udp.dstport
					srcPort = udp.srcport
					if dstPort == 53 or srcPort == 53:
						if dstIp == '100.0.0.20' or dstIp == '100.0.0.21' or dstIp == '100.0.0.22' or dstIp == '100.0.0.25' or srcIp == '100.0.0.20' or srcIp == '100.0.0.21' or srcIp == '100.0.0.22' or srcIp == '100.0.0.25': 
							super(LearningFireWall1,self)._handle_PacketIn(event)
							log.debug("f1 p1: A packet is transmitted to (%s) port (%s) by udp protocol." %(dstIp,dstPort))
							print("f1 p1: A packet is transmitted to (%s) port (%s) by udp protocol:Success." %(dstIp, dstPort))		
							return
						else:
							log.debug("f1 p1: A packet is transmitted to (%s) port (%s) by udp protocol:DROP." %(dstIp, dstPort))
							drop()
							print("f1 p1: A packet is transmitted to (%s) port (%s) by udp protocol:drop." %(dstIp, dstPort))
							return
					else:
						drop()
						print("f1 p1: A packet is transmitted to (%s) port (%s) by udp protocol:drop." %(dstIp, dstPort))
				
			else:
				log.debug("f1 p1: A packet is not transmitted by ipv4:DROP." )
				drop()
				return
		
		# firewall in port 2 (DmZ to PbZ)	
		elif event.port == 2:
			if packet.find("arp"):
				a = packet.find("arp")
				if a.opcode == a.REPLY or a.opcode == a.REQUEST:
					super(LearningFireWall1, self)._handle_PacketIn(event)
					return
			ip = packet.find('ipv4')
			if ip is not None:
				icmp = ip.find('icmp')
				if icmp is not None:
					dstIp = ip.dstip
					srcIp = ip.srcip
					if icmp.type == 0:			
						if dstIp == '100.0.0.20' or dstIp =='100.0.0.21' or dstIp == '100.0.0.22' or dstIp == '100.0.0.25' or dstIp == '100.0.0.40' or dstIp =='100.0.0.41' or dstIp == '100.0.0.42' or dstIp == '100.0.0.45':
							drop()
							print("f1 p2: An ICMP response packet is transmitted from (%s) to (%s) by icmp protocol:drop." %(srcIp,dstIp))
							return
						else:
							super(LearningFireWall1, self)._handle_PacketIn(event)
							return
					elif icmp.type == 8:
						if dstIp == '100.0.0.11' or dstIp == '100.0.0.10':
							super(LearningFireWall1, self)._handle_PacketIn(event)	 
							print("f1 p2: An ICMP request packet is transmitted from (%s) to (%s) by icmp protocol:Success." %(srcIp,dstIp))
							return
						else:
							drop()
							return
					else:
						drop()
						return
				udp = ip.find('udp')
				if udp is not None:
					log.debug("f1 p2: A packet is transmitted by udp protocol.")
					dstIp = ip.dstip
					dstPort = udp.dstport
					
					super(LearningFireWall1, self)._handle_PacketIn(event)
					print("f1 p2: A packet is transmitted to (%s) port (%s) by udp protocol:Success." %(dstIp, dstPort))
					return
					#else:
						#drop()
						#print("A packet is transmitted to (%s) port (%s) by udp protocol:drop." %(dstIp, dstPort))
						#return

				tcp = ip.find('tcp')
				if tcp is not None:
					print("f1 p2: A packet is transmitted by tcp protocol.")
					log.debug("f1 p2: A packet is transmitted by tcp protocol.")
					dstIp = ip.dstip
					dstPort = tcp.dstport
					print("f1 p2: ip: %s === port: %s" %(dstIp,dstPort))	
					super(LearningFireWall1, self)._handle_PacketIn(event)
					print("f1 p2: A packet is transmitted to (%s) port (%s) by tcp protocol:success." %(dstIp,dstPort))
					return
					#else:
						#print("A packet is transmitted to (%s) port (%s) by tcp protocol:drop" %(dstIp,dstPort))
						#drop()
						#return

				else:
					log.debug("f1 p2: A packet is transmitted by other kind of protocol:DROP.")
					drop()
					return
			
			else:
				log.debug("f1 p2: A packet is not transmitted by ipv4:DROP.")
				drop()
				return
