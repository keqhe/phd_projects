set terminal postscript eps enhanced color 'Roman,30';
set size ratio 0.625
set output "hp_outbound_dec_r2.eps"
#set ylabel "CDF";
set ylabel "latency (ms)";
set xlabel "openflow rule #"
#set logscale x
#set logscale y
set xrange [0:750];
set yrange [0:1500];


#set xtics ("200" 200, "400" 400, "600" 600, "800" 800, "1000" 1000)

set key top right
#set key horizontal bottom
plot "hp_dec_proactive.txt" using 1:2 title "insertion rate = 2/s" with points pointtype 1 pointsize 0.5
