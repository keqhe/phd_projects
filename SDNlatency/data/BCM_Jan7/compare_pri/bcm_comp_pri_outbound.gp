set terminal postscript eps enhanced color 'Roman,30';
set size ratio 0.625
set output "bcm_comp_pri_outbound_rate50.eps"
#set ylabel "CDF";
set ylabel "latency (ms)";
set xlabel "openflow rule #"
#set logscale x
set logscale y
set xrange [0:768];
set yrange [0.1:100000];


#set xtics ("200" 200, "400" 400, "600" 600, "800" 800, "1000" 1000)

set key top right
#set key horizontal bottom
plot "BCM_same_rate50_acc_outbound.txt" using 1:2 title "same pri" with points pointtype 1 pointsize 0.5,\
"BCM_incr_rate50_acc_outbound.txt" using 1:2 title "incr pri" with points pointtype 2 pointsize 0.5,\
"BCM_dec_rate50_acc_outbound.txt" using 1:2 title "decr pri" with points pointtype 3 pointsize 0.5

