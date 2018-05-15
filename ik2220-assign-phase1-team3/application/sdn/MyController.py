from pox.core import core
from pox.forwarding.l2_learning import LearningSwitch
from Firewall1 import LearningFireWall1
from Firewall2 import LearningFireWall2

def launch ():
	controller = MyController()
	core.register("MyController", controller)
class MyController (object):
	def __init__ (self):
		core.openflow.addListeners(self)

	def _handle_ConnectionUp (self, event):
		dpid = event.dpid

		if dpid == 1 or dpid == 3 or dpid == 4 or dpid == 5 or dpid == 6 or dpid == 7 or dpid == 8 or dpid == 10 or dpid == 11:
			LearningSwitch(event.connection, False)

		elif dpid == 2:
			LearningFireWall1(event.connection)

		elif dpid == 9:
			LearningFireWall2(event.connection)
		else:
			print("Unknown device.")



