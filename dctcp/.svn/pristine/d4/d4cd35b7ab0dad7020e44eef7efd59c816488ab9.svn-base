#!/usr/bin/bash

#dirs="dctcp ours ours16"
dirs=$1
flows="5000"
#runs="20"
runs="20"
sender="8"
receiver="19"

for f in ${flows[@]}; do
	for d in ${dirs[@]}; do
		echo "Dir: $d Flows: $f"
		#python run-dumbbell-threaded.py --dir dctcp-$f --flows $f --runs $runs --exptime $exptime
		echo "Sender $sender"
		grep Avera $d-$f/run00*/cpustat-dcn$sender.txt  | awk '{s+=$NF}END{print s/NR}'
		
		echo "Receiver $receiver"
		grep Avera $d-$f/run00*/cpustat-dcn$receiver.txt  | awk '{s+=$NF}END{print s/NR}'

		echo "Throughput (Mbps)"
		cat $d-$f/run00*/dcn$sender-dcn$receiver-flow$f | grep Mbps | awk -v r=$runs '{s+=$(NF-1)}END{print s/r}'
	
		echo ""
	
	done
done
