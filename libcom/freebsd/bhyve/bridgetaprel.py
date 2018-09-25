#!/usr/bin/env python3.6
# specify interfaces that need real interface connectivity with vlan tagging
ifffwan={'parent': 'em0', 'vlanid': 10, 'bridgename': 'bridge8'}
# specify to which bridges a guest should be connected.
# same index thing as with nodes
gatewaybridges=[['g0','bridge1','bridge2','bridge3','bridge4','bridge5','bridge6']]
for gateway in range(len(gatewaybridges)):
    print(gatewaybridges[gateway])
# first element with index [0] is node0 so keep that in mind. This matrices don't have keys sadly
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
for (i, node) in enumerate(nodebridges):
    for (j, bridge) in enumerate(node):
        #print(i,j,bridge)
        if j==0:
            elementname=nodebridges[j]
            print('current element: ',bridge)
            continue
        print('ifconfig statement ',nodebridges[i][j])
