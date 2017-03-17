set terminal postscript eps enhanced color 'Roman,30';
set size ratio 0.625
set output "bcm_same_pri_outbound_rate200.eps"
#set ylabel "CDF";
set ylabel "latency (ms)";
set xlabel "openflow rule #"
#set logscale x
#set logscale y
set xrange [0:768];
set yrange [0:2000];


#set xtics ("200" 200, "400" 400, "600" 600, "800" 800, "1000" 1000)

set key top right
#set key horizontal bottom
plot "BCM_same_rate200_acc_outbound.txt" using 1:2 title "insertion rate = 200/s" with points pointtype 1 pointsize 0.5

