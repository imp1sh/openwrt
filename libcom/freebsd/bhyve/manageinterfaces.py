#!/usr/bin/env python3.6
# for FreeBSD
import subprocess
import os
import sys
# configure to your needs
# specify interfaces that need real interface connectivity with vlan tagging
# 0 interface name 1 parent interface name 2 vlan id 3 bridge name
realinterfaces=[
        ['iflcwan', 'em0', 10, 'bridge8'],
        ['iflcadm', 'em0', 300, 'bridge7'],
        ['iflcn4', 'em0', 200, 'bridge2'],
        ['iflcn5', 'em0', 201, 'bridge1']]
# specify to which bridges a guest should be connected.
gatewaybridges=[['g0','bridge1','bridge2','bridge3','bridge4','bridge5','bridge6']]
# first element with index [0] is node0 so keep that in mind.
nodebridges=[
        # the first index is always the node name followed by the interfaces
        ['node0','bridge6','bridge13'],
        ['node1','bridge5','bridge18','bridge21'],
        ['node2','bridge4','bridge23'],
        ['node3','bridge3','bridge27','bridge29'],
        ['node4','bridge2','bridge32'],
        ['node5','bridge9'],
        ['node6','bridge9','bridge10'],
        ['node7','bridge10','bridge11'],
        ['node8','bridge11','bridge12'],
        ['node9','bridge12'],
        ['node10','bridge13','bridge14'],
        ['node11','bridge14','bridge15'],
        ['node12','bridge15','bridge16','bridge17'],
        ['node13','bridge16'],
        ['node14','bridge18','bridge19','bridge22'],
        ['node15','bridge17','bridge19','bridge20'],
        ['node16','bridge20'],
        ['node17','bridge21','bridge22','bridge23','bridge24','bridge25','bridge26'],
        ['node18','bridge24'],
        ['node19','bridge26','bridge27','bridge30','bridge31'],
        ['node20','bridge25','bridge28'],
        ['node21','bridge28'],
        ['node22','bridge29','bridge30','bridge32','bridge33'],
        ['node23','bridge31','bridge33']]
# end config

# action can be create or destroy
action=sys.argv[1]
if (action!="create") and (action!="destroy"):
    print("Please give either create or destroy as parameter.")
    exit()
#determine all bridges to create
bridgelist=[]
for (i, interface) in enumerate(realinterfaces):
    bridgelist.append(realinterfaces[i][3])
for (i, node) in enumerate(nodebridges):
    for (j,bridge) in enumerate(node):
        if j==0:
            continue
        bridgelist.append(nodebridges[i][j])
for (i, gateway) in enumerate(gatewaybridges):
    for (j, bridge) in enumerate(gateway):
        if j==0:
            continue
        bridgelist.append(gatewaybridges[i][j])
#print(sorted(set(bridgelist)))
# handle bridges, destroy or create
bridgelist=sorted(set(bridgelist))
for bridgename in bridgelist:
    shellbridge="sudo ifconfig {0} {1}".format(bridgename,action)
    os.system(shellbridge)
# handle tap interfaces, destroy or create
if action=="create":
    open("currentnetwork.txt", "w").close()
    # gateways
    for (i, gateway) in enumerate(gatewaybridges):
        for (j, bridge) in enumerate(gateway):
            if j==0:
                gatewayname=gatewaybridges[i][j]
                continue
            # create new tap
            returntapcreate=subprocess.run(["sudo", "ifconfig", "tap", "create"], stdout=subprocess.PIPE)
            tapinterface=returntapcreate.stdout.decode('utf-8')
            tapinterface=tapinterface.rstrip()
            # assign tap to bridge
            shellbridgetap="sudo ifconfig {0} addm {1}".format(gatewaybridges[i][j],tapinterface)
            # write into file what has been done
            with open("currentnetwork.txt", "a") as currentfile:
                fileline="{0} has {1} on {2}\n".format(gatewayname,tapinterface,gatewaybridges[i][j])
                currentfile.write(fileline)
            os.system(shellbridgetap)
    # nodes
    for (i, node) in enumerate(nodebridges):
        for (j, bridge) in enumerate(node):
            #print(i,j,bridge)
            if j==0:
                nodename=nodebridges[i][j]
                continue
            # create new tap
            returntapcreate=subprocess.run(["sudo", "ifconfig", "tap", "create"], stdout=subprocess.PIPE)
            tapinterface=returntapcreate.stdout.decode('utf-8')
            tapinterface=tapinterface.rstrip()
            # assign tap to bridge
            shellbridgetap="sudo ifconfig {0} addm {1}".format(nodebridges[i][j],tapinterface)
            # write into file what has been done
            with open("currentnetwork.txt", "a") as currentfile:
                fileline="{0} has {1} on {2}\n".format(nodename,tapinterface,nodebridges[i][j])
                currentfile.write(fileline)
            os.system(shellbridgetap)
elif action=="destroy":
    taplist=[]
    with open("currentnetwork.txt") as currentfile:
        for line in currentfile:
            field=line.split()
            taplist.append(field[2])
    taplist=sorted(set(taplist))
    for tapname in taplist:
        shelltap="sudo ifconfig {0} destroy".format(tapname)
        os.system(shelltap)
    # empty file after tap and bridge are deleted
    open("currentnetwork.txt", "w").close()
# example line for creating real interface
# sudo ifconfig em0.10 create vlan 10 vlandev em0 name iflcwan
