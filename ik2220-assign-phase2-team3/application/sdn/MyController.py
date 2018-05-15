from pox.core import core
from pox.forwarding.l2_learning import LearningSwitch
from Firewall1 import LearningFireWall1
from Firewall2 import LearningFireWall2
from subprocess import Popen
import os

log = core.getLogger()
def launch ():
	controller = MyController()
	core.register("MyController", controller)
class MyController (object):
	def __init__ (self):
		core.openflow.addListeners(self)

	def _handle_ConnectionUp (self, event):
		dpid = event.dpid

		if(dpid == 2 or dpid == 9):
			log.debug("Firewall triggered:")
			if(dpid == 2):
				LearningFireWall1(event.connection)
				log.debug("This is firewall 1.")
			else:
				LearningFireWall2(event.connection)
				log.debug("This is firewall 2.")
		
		elif (dpid == 1 or dpid == 3 or dpid == 5 or dpid == 8 or dpid == 11):
			LearningSwitch(event.connection, False)
			log.debug("Switch triggered.")
		
		elif (dpid == 4):
			#LearningSwitch(event.connection, False)
			Popen(["sudo","/usr/local/bin/click","/home/click/ik2220-assign-phase2-team3/application/nfv/lb.click","Name=s4","MAC0=03","port=53","proto=udp","MAC1=04","VIP=100.0.0.25","DIP0=100.0.0.20","DIP1=100.0.0.21","DIP2=100.0.0.22","Report=lb1"])
			log.debug("Load balancer DNS Servers triggered.",dpid)
		elif (dpid == 7):
			#LearningSwitch(event.connection, False)
			Popen(["sudo","/usr/local/bin/click","/home/click/ik2220-assign-phase2-team3/application/nfv/lb.click","Name=s7","MAC0=05","port=80","proto=tcp","MAC1=06","VIP=100.0.0.45","DIP0=100.0.0.40","DIP1=100.0.0.41","DIP2=100.0.0.42","Report=lb2"])
			log.debug("Load Balancer Web Servers triggered.")
		elif (dpid == 6):
			#LearningSwitch(event.connection, False)
			Popen(["sudo","/usr/local/bin/click","/home/click/ik2220-assign-phase2-team3/application/nfv/ids.click"])
			log.debug("IDS triggered.")
		elif (dpid == 10):
			#Popen(["click",path+"napt.click"])
			#LearningSwitch(event.connection, False)
			Popen(["sudo","/usr/local/bin/click","/home/click/ik2220-assign-phase2-team3/application/nfv/napt.click"])
			log.debug("NAPT triggered.")
		else:
			log.debug("Network entity is an unknown entity", dpid)




