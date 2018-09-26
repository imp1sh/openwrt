#!/usr/bin/env bash
# manage interfaces so destroy or create them
if [ $# -eq 0 ]; then
	echo "no parameter given. please specify. create or destroy."
	exit 1
fi
maxbridge="40"
maxtap="200"
source bridgetaprel.bash
if [ $1 == "create" ]; then
	> currentnetwork
	for bridgenumber in $(seq 1 ${maxbridge}); do 
		ifconfig bridge${bridgenumber} create
	done
	for gatewayindex in $(seq 1 ${maxgateway}); do
		currentgateway="g${gatewayindex}"
		for currentbridgenumber in $(echo "${!currentgateway}"); do
			currenttap=$(ifconfig tap create)
			ifconfig bridge${currentbridgenumber} addm ${currenttap}
			echo "Gateway g${gatewayindex} has ${currenttap} on bridge${currentbridgenumber}" >> currentnetwork
		done
	done
	for nodeindex in $(seq 1 ${maxnode}); do
		# first of all, get all the bridge names that are relevant for the current node
		currentnode="n${nodeindex}"
		for currentbridgenumber in $(echo "${!currentnode}"); do
			currenttap=$(ifconfig tap create)
			ifconfig bridge${currentbridgenumber} addm ${currenttap}
			echo "Node n${nodeindex} has ${currenttap} on bridge${currentbridgenumber}" >> currentnetwork
		done
		echo "current node index is $nodeindex"
	done
	# ergebnis
	# ifconfig tap create und das in variable einlesen
	# Ergebnis davon k�nnte z.B. tap1 sein, das ist im Endeffekt immer das nächste freie tap interface
	# ifconfig bridge6 addm <<eingelesenen Wert>>
	# könnte sein ifconfig bridge6 addm tap1
	# configure real interfaces
        for realinterface in ${realinterfaces[*]}; do
		# realinterface is in this example ffwan
		# $ffwan[0] is parent interface, in this example em0
		# $ffwan[1] is vlan id, in this example 10
		# $ffwan[2] is bridge name it shall get attached to, in this example bridge8
		ifconfig ${!realinterface[0]}.${realinterface[1]} create vlan ${!realinterface[1]} vlandev ${!realinterface[0]} name $realinterface
		ifconfig ${!realinterface[2]} 2&> /dev/null
		if [ $? -ne 0 ]; then
			ifconfig ${!realinterface[2]} create
		fi
		ifconfig ${!realinterface[2]} addm $realinterface
		# ifconfig em0.10 create vlan 10 vlandev em0 name ffwan
	done
else
	for bridgenumber in $(seq 1 ${maxbridge}); do 
		ifconfig bridge${bridgenumber} destroy
	done
	for tapindex in $(seq 0 ${maxtap}); do
		ifconfig tap${tapindex} destroy
	done
	> currentnetwork
fi
