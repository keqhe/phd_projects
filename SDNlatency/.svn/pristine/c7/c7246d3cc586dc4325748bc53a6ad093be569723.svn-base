set terminal postscript eps enhanced color 'Roman,30';
set size ratio 0.625
set output "hp_inbound_delay_200.eps"
#set ylabel "CDF";
set ylabel "latency (ms)";
set xlabel "openflow rule #"
#set logscale x
#set logscale y
set xrange [1:1000];
set yrange [0:150];


set xtics ("200" 200, "400" 400, "600" 600, "800" 800, "1000" 1000)

set key top right
#set key horizontal bottom
plot "hp_packet_in_delays.txt" using 1:3 title "flow rate = 200/s" with points pointtype 1 pointsize 1  lc rgb "black"
