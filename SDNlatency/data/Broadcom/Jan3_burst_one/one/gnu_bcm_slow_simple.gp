set terminal postscript eps enhanced color 'Roman,30';
set size ratio 0.625
set output "bcm_slow_simple.eps"
#set ylabel "CDF";
set ylabel "latency (ms)";
set xlabel "openflow rule #"
#set logscale x
#set logscale y
set xrange [1:768];
set yrange [0.1:100];


#set xtics ("10" 20, "20" 40, "30" 60, "40" 80, "50" 100, "60" 120, "70" 140)

#set key top right
#set key horizontal bottom
plot "bcm_slowest_simple.txt" using 1:2 title "1-flow/sec" with linespoints linetype 1 linecolor 3 linewidth 3 pointtype 1 pointsize 0.1
