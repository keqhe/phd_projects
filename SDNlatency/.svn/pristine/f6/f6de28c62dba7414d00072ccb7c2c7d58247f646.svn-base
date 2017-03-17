set terminal postscript eps enhanced color 'Roman,30';
set size ratio 0.625
set output "bcm_two_pri_outbound_burst.eps"
#set ylabel "CDF";
set ylabel "latency (ms)";
set xlabel "openflow rule #"
#set logscale x
#set logscale y
set xrange [0:768];
set yrange [0:50000];


#set xtics ("200" 200, "400" 400, "600" 600, "800" 800, "1000" 1000)

set key top right
#set key horizontal bottom
plot "BCM_two_pri_mod_0.txt" using 1:2 title "priority low" with points pointtype 1 pointsize 0.5, \
"BCM_two_pri_mod_1.txt" using 1:2 title "priority high" with points pointtype 2 pointsize 0.5

