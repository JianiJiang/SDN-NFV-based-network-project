from pox.core import core
from pox.forwarding.l2_learning import LearningSwitch
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt

log = core.getLogger()
class LearningFireWall2 (LearningSwitch):
	def __init__ (self, connection):
		LearningSwitch.__init__(self, connection, False)
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

		# firewall in port 1 (from DmZ to PrZ)
		if event.port == 1:
			if packet.find("arp"):
				a = packet.find("arp")
				if a.opcode == a.REPLY or a.opcode == a.REQUEST:
					super(LearningFireWall2, self)._handle_PacketIn(event)
					return
			ip = packet.find('ipv4')
			if ip is not None:
				icmp = ip.find('icmp')
				if icmp is not None:
					dstIp = ip.dstip
					if icmp.type == 8:
						if dstIp == '100.0.0.11' or dstIp =='100.0.0.12':
							super(LearningFireWall2, self)._handle_PacketIn(event)	 
							print("f2 p1: request icmp packet transmiited successful.")
							return
						else:
							drop()
							print("f2 p1: A packet is transmitted to (%s) by icmp protocol:DROP." %dstIp)
							return
				
					elif icmp.type == 0:
						super(LearningFireWall2, self)._handle_PacketIn(event)
						print("f2 p1: response icmp packet transmitted successful.")
						return
				
					#else:
						#log.debug("f2 p1: A packet is transmitted to (%s) by icmp protocol:DROP." %dstIp)
						#drop()
						#return
				tcp = ip.find('tcp')
				if tcp is not None:
					log.debug("f2 p1: A packet is transmitted by tcp protocol.")
					dstIp = ip.dstip
					dstPort = tcp.dstport
					#if dstPort == 80 or dstPort == 53:
					super(LearningFireWall2, self)._handle_PacketIn(event)
					log.debug("f2 p1: A packet is transmitted to (%s) port (%s) by tcp protocol." %(dstIp,dstPort))
					print("f2 p1: A packet is transmitted to (%s) port (%s) by tcp protocol:Success." %(dstIp, dstPort))
					return

					#else:
						#log.debug("A packet is transmitted to (%s) port (%s) by tcp protocol:DROP." %(dstIp, dstPort))
						#drop()
						#print("A packet is transmitted to (%s) port (%s) by tcp protocol:drop." %(dstIp, dstPort))
						#return
					
				udp = ip.find('udp')
				if udp is not None:
					log.debug("f2 p1: A packet is transmitted by udp protocol.")
					dstIp = ip.dstip
					dstPort = udp.dstport
					#if dstPort == 53:
						#if dstIp == '100.0.0.20' or dstIp == '100.0.0.21' or dstIp == '100.0.0.22': 
					super(LearningFireWall2,self)._handle_PacketIn(event)
					log.debug("f2 p1: A packet is transmitted to (%s) port (%s) by udp protocol." %(dstIp,dstPort))		
					print("f2 p1: A packet is transmitted to (%s) port (%s) by udp protocol:Success." %(dstIp, dstPort))
					return
					#else:
						#log.debug("A packet is transmitted to (%s) port (%s) by udp protocol:DROP." %(dstIp, dstPort))
						#drop()
						#print("A packet is transmitted to (%s) port (%s) by udp protocol:drop." %(dstIp, dstPort))
						#return

				

			else:
				log.debug("f2 p1: A packet is not transmitted by ipv4:DROP." )
				drop()
				return
		
		# firewall in port 2 (PrZ to DmZ)	
		elif event.port == 2:
			if packet.find("arp"):
				a = packet.find("arp")
				if a.opcode == a.REPLY or a.opcode == a.REQUEST:
					super(LearningFireWall2, self)._handle_PacketIn(event)
					return

			ip = packet.find('ipv4')
			if ip is not None:
				icmp = ip.find('icmp')
				if icmp is not None:
					dstIp = ip.dstip
					if icmp.type == 0:			
						if dstIp == '100.0.0.11' or dstIP =='100.0.0.12':
							super(LearningFireWall2, self)._handle_PacketIn(event)
							return
						else:
							drop()
							return
					
					elif icmp.type == 8:
						if dstIp == '100.0.0.11' or dstIp =='100.0.0.12':
							super(LearningFireWall2, self)._handle_PacketIn(event)	 
							print("f2 p2: request icmp packet is transmitted successful.")
							return
					#else:
						#drop()
						#print("f2 p2: request icmp packet is: drop.")
						#return

				udp = ip.find('udp')
				if udp is not None:
					log.debug("f2 p2: A packet is transmitted by udp protocol.")
					dstIp = ip.dstip
					srcIp = ip.srcip
					dstPort = udp.dstport
					srcPort = udp.srcport
					if dstPort == 53 or srcPort == 53:
						if dstIp =='100.0.0.20' or dstIp =='100.0.0.21' or dstIp=='100.0.0.22' or srcIp == '100.0.0.20' or srcIp == '100.0.0.21' or srcIp == '100.0.0.22':
							super(LearningFireWall2, self)._handle_PacketIn(event)
							print("f2 p2: A packet is transmitted to (%s) port (%s) by udp protocol:Success." %(dstIp, dstPort))
							return
						else:
							drop()
							print("f2 p2: A packet is sent by udp to a wrong dst ip.")
					else:
						drop()
						print("f2 p2: A packet is transmitted to (%s) port (%s) by udp protocol:drop." %(dstIp, dstPort))
						return


				tcp = ip.find('tcp')
				if tcp is not None:
					print("f2 p2: A packet is transmitted by tcp protocol.")					
					log.debug("f2 p2: A packet is transmitted by tcp protocol.")
					dstIp = ip.dstip
					dstPort = tcp.dstport
					print("f2 p2: IP: %s ===== port: %s" %(dstIp,dstPort))
					f = tcp.ACK
					print("The ACK flag is %s" %f)
					if f== False:
						if dstPort == 80:
							if dstIp == '100.0.0.40' or dstIp == '100.0.0.41' or dspIp == '100.0.0.42':
								super(LearningFireWall2, self)._handle_PacketIn(event)
								print("f2 p2: A packet is transmitted to (%s) port (%s) by tcp protocol:success." %(dstIp,dstPort))
								log.debug("f2 p2: A packet is transmitted to (%s) port (%s) by tcp protocol." %(dstIp,dstPort))
								return
							else:
								log.debug("f2 p2: A packet is transmitted to (%s) port (%s) by tcp protocol:DROP." %(dstIp, dstPort))
								drop()
								print("f2 p2: A packet is transmitted to (%s) port (%s) by tcp protocol:drop." %(dstIp, dstPort))
								return

						else:
							print("f2 p2: A packet is transmitted to (%s) port (%s) by tcp protocol:DROP." %(dstIp, dstPort))
							log.debug("f2 p2: A packet is transmitted to (%s) port (%s) by tcp protocol:DROP." %(dstIp, dstPort))
							drop()
							return
					elif f == True:
						super(LearningFireWall2, self)._handle_PacketIn(event)
						print("f1 p2: A ACK packet is transmitted to (%s) port (%s) by tcp protocol:success." %(dstIp,dstPort))
						return

			else:
				log.debug("f2 p2: A packet is not transmitted by ipv4:DROP.")
				drop()
				return
			
