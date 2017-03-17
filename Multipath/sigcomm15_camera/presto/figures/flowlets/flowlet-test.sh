#!/bin/bash
usage()
{
    echo "Usage: $0 numhosts"
    exit
}

if [ $# != 1 ]; then
    usage
fi

#
# To be run on arldcn26. (but I actually ran on the src, arldcn3-- could be bug, last line, on arldcn26)
#  Do a 'scp' xfer between src and dst. Then have varying number of 
#    background hosts, with nuttcp xfer from backhosts[i] to dst.
# Want to get flowlet size on sender.
# Uses optimal topology.

#sending hosts only
backhosts=( 4 5 6 7 8 9 10 1 )

#sender for scp flow
src=3

#sink host for everything
dst=20

#number of background hosts to run on this run
numhosts=$1

#result dir
basedir="/presto/erozner/flowlets"
prefix="testrun"
rundir="$basedir/run$prefix-hosts$numhosts"

#get seq to work correctly
numhosts=$(( $numhosts - 1 ))

#create result directory
ssh arldcn$src "mkdir -p $rundir"

#kill tcpdump if it is running
for h in "${backhosts[@]}"
do
	echo $h
	ssh arldcn$h sudo killall nuttcp &
done
sleep 2

#ssh into sink
echo "arldcn$dst nuttcp server start"
ssh arldcn$dst "sudo killall nuttcp ; nuttcp -S"

#start tcpdump on the sender
ssh arldcn$src "sudo tcpdump -i tcpdump -i eth3 -w $rundir/flowlet.pcap -s 100 -K" &
sleep 5

#start nuttcp on background senders and let them warm up
for i in `seq 0 $numhosts`
do
	echo Starting on index $i host ${backhosts[$i]}
	ssh arldcn${backhosts[$i]} "nuttcp -t -T 9999 -i 1 10.3.1.$dst" > $rundir/nuttcp-${backhosts[$i]} &
	sleep 0.5
done

#sleep to warm up
sl=10
echo Sleep $sl seconds
sleep $sl

echo Starting scp: ssh arldcn$dst "scp 10.3.1.$src:/tmp/1G.img /tmp"
#start scp... want dst to request from src
ssh arldcn$dst "scp 10.3.1.$src:/tmp/1G.img /tmp"
echo "scp done"

#kill everything, nuttcp and tcpdump on sender
for i in `seq 0 $numhosts`
do
	ssh arldcn${backhosts[$i]} "sudo killall nuttcp" 2> /dev/null &
done
ssh arldcn$src "sudo killall tcpdump"
sleep 2

#parse results ... XXX safe for ssh'ing? 
python get-intervals.py 0.000500 $rundir/flowlet.pcap $src > $rundir/flowlets
cat $rundir/flowlets | awk '{print $NF}' | sort -n > $rundir/fl
