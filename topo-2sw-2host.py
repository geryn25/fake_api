"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.node import CPULimitedHost
import time
import os

class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()

class MyTopo( Topo ):
    "Simple topology example."

    def build( self ):
        "Create custom topo."

	defaultIP = '192.168.1.1/24'  # IP address for r0-eth1
        router = self.addNode( 'r0', cls=LinuxRouter, ip=defaultIP )

        # Add hosts and switches
        h1 = self.addHost( 'server', ip='192.168.1.100/24',
                           defaultRoute='via 192.168.1.1',max_queue_length=100 )
        h2 = self.addHost( 'user', ip='172.16.0.100/12',
                           defaultRoute='via 172.16.0.1',max_queue_length=100 )
	

        # Add links
        self.addLink( h1, router, intfName2='r0-eth1',
                      params2={ 'ip' : defaultIP }, bw=2 )  # for clarity
        self.addLink( h2, router, intfName2='r0-eth2',
                      params2={ 'ip' : '172.16.0.1/12' },bw =1000 )

def runTopo():
	os.system=('mn -c')

	topo=MyTopo()
	net = Mininet(topo=topo,host=CPULimitedHost, link=TCLink)
	net.start()

	#print net['server'].cmd('sysctl -w net.ipv4.tcp_congestion_control=[cubic]')
	#print net['user'].cmd('sysctl -w net.ipv4.tcp_congestion_control=[cubic]')

	user,server=net.get('user','server')
	CLI(net)
	net.stop()

if __name__=='__main__':
	setLogLevel('info')
	runTopo()


	
	

