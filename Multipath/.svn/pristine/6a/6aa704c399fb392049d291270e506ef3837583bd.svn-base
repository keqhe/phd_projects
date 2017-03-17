mv scp.data scp.data.bak 2> /dev/null

for i in `seq 1 8`
do
	echo "run $i"
	./flowlet-test.sh $i
	printf "$i " >> scp.data
	cat runtestrun-hosts$i/fl | sort -n -r | awk '{print $1/1000000}' | sed ':a;N;$!ba;s/\n/ /g' >> scp.data
done

