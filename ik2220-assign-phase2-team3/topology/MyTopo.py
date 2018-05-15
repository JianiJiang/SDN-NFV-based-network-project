from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.node import OVSSwitch
import sys
import time
import os


class MyTopo(Topo):	
	def __init__(self):
	
	#initialize topology
		Topo.__init__(self)
 
	#add hosts and switches
	#public zone
		sw1= self.addSwitch('s1')
		h1=self.addHost('h1',ip='100.0.0.10/24',mac='00:00:00:00:00:10', defaultRoute='via 100.0.0.1')
		h2=self.addHost('h2',ip='100.0.0.11/24', mac='00:00:00:00:00:11', defaultRoute='via 100.0.0.1')
		fw1=self.addSwitch('s2')

	#demilitarized zone
		sw2=self.addSwitch('s3')
		lb1=self.addSwitch('s4')
		sw3=self.addSwitch('s5')
		ids=self.addSwitch('s6')
		insp=self.addHost('insp', ip='100.0.0.30/24', mac='00:00:00:00:00:30')
		lb2=self.addSwitch('s7')
		sw4=self.addSwitch('s8')
		ds1=self.addHost('ds1',ip='100.0.0.20/24', mac='00:00:00:00:00:20')
		ds2=self.addHost('ds2',ip='100.0.0.21/24', mac='00:00:00:00:00:21')
		ds3=self.addHost('ds3',ip='100.0.0.22/24', mac='00:00:00:00:00:22')
		ws1=self.addHost('ws1',ip='100.0.0.40/24', mac='00:00:00:00:00:40')
		ws2=self.addHost('ws2',ip='100.0.0.41/24', mac='00:00:00:00:00:41')
		ws3=self.addHost('ws3',ip='100.0.0.42/24', mac='00:00:00:00:00:42')

	# private zone
		fw2=self.addSwitch('s9')
		napt=self.addSwitch('s10')
		sw5=self.addSwitch('s11')
		h3=self.addHost('h3',ip='10.0.0.50/24',mac='00:00:00:00:00:50', defaultRoute='via 10.0.0.1')
		h4=self.addHost('h4',ip='10.0.0.51/24', mac='00:00:00:00:00:51', defaultRoute='via 10.0.0.1')

		
	# public links
		self.addLink(h1,sw1)
		self.addLink(h2,sw1)
		self.addLink(sw1,fw1)
		self.addLink(fw1,sw2)

	# Demilitarized Zone
		self.addLink(sw2,lb1)
		self.addLink(lb1,sw3)
		self.addLink(sw3,ds1)
		self.addLink(sw3,ds2)
		self.addLink(sw3,ds3)
		self.addLink(sw2,ids)
		self.addLink(ids,insp)
		self.addLink(ids,lb2)
		self.addLink(lb2,sw4)
		self.addLink(sw4,ws1)
		self.addLink(sw4,ws2)
		self.addLink(sw4,ws3)

		self.addLink(sw2,fw2)
		self.addLink(fw2,napt)
		self.addLink(napt,sw5)

	# private zone
		self.addLink(sw5,h3)
		self.addLink(sw5,h4)
		


def Phase2():
	c0 = RemoteController('c0', ip='127.0.0.1', port=6633)
	net = Mininet(topo=MyTopo(), controller=c0, switch=OVSSwitch)

	net.start()
	ds1 = net.get('ds1')
	ds2 = net.get('ds2')
	ds3 = net.get('ds3')
	ws1 = net.get('ws1')
	ws2 = net.get('ws2')
	ws3 = net.get('ws3')

	ds1.cmd('python ds1.py &')
	ds2.cmd('python ds2.py &')
	ds3.cmd('python ds3.py &')
	ws1.cmd('python -m SimpleHTTPServer 80 &')
	ws2.cmd('python -m SimpleHTTPServer 80 &')
	ws3.cmd('python -m SimpleHTTPServer 80 &')

	CLI(net)

	net.stop()

if __name__ == '__main__':
	setLogLevel('info')
	Phase2()
