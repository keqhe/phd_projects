#!/usr/bin/bash

flows="5000"
exptime="30"  #has to be 30 b/c it is hardcoded into threaded-sender.c
runs="10"
dir="acdctcp2"

for f in ${flows[@]}; do
	echo "Flows: $f exptime: $exptime runs: $runs"
	python run-dumbbell-threaded.py --dir $dir-$f --flows $f --runs $runs --exptime $exptime

done
