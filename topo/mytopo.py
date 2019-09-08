#!/usr/bin/env python

from mininet.net import Containernet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel

from functools import partial


setLogLevel('info')

net = Containernet(controller=partial(RemoteController, ip='192.168.56.1', port=6633))

info('*** Adding controller\n')
net.addController('c0')

info('*** Adding docker containers using ubuntu:trusty images\n')

h1 = net.addDocker('h1', ip='210.0.0.101', dimage="mg-host-base")
h2 = net.addDocker('h2', ip='210.0.0.102', dimage="mg-host-base")

gw1 = net.addDocker('gw1', ip='210.0.0.200', dimage="mg-ids", pubnet=True)
gw2 = net.addDocker('gw2', ip='210.0.0.200', dimage="mg-base", pubnet=True)

info('*** Adding switches\n')
s1 = net.addSwitch('sw1')
s2 = net.addSwitch('sw2')

info('*** Creating links\n')

net.addLink(h1, s1)
net.addLink(gw1, s1)

net.addLink(h2, s2)
net.addLink(gw2, s2)

net.addLink(s1, s2, latency=200)

# net.addLink(s1, s2, cls=TCLink, delay='100ms', bw=1)

info('*** Starting network\n')
net.start()

# info('*** Testing connectivity\n')
# net.ping([h1, h2])

info('*** Starting nodes\n')
h1.start()
h2.start()
gw1.start()
gw2.start()

info('*** Running CLI\n')
CLI(net)

info('*** Stopping network')
net.stop()


