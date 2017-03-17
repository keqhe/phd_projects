set terminal postscript eps enhanced color 'Roman,30';
set size ratio 0.625
set output "compare_priority_bcm_simple.eps"
#set ylabel "CDF";
set ylabel "latency (ms)";
set xlabel "openflow rule #"
#set logscale x
set logscale y
set xrange [1:768];
set yrange [0.1:100000];


#set xtics ("10" 20, "20" 40, "30" 60, "40" 80, "50" 100, "60" 120, "70" 140)

set key top right
#set key horizontal bottom
plot "compare_priority_bcm.txt" using 1:2 title "same pri." with linespoints linetype 1 linecolor 3 linewidth 3 pointtype 1 pointsize 0.1, \
"compare_priority_bcm.txt" using 1:3 title "decrease pri." with linespoints linetype 1 linecolor 4 linewidth 3 pointtype 3 pointsize 0.1,\
"compare_priority_bcm.txt" using 1:4 title "incease pri." with linespoints linetype 1 linecolor 5 linewidth 3 pointtype 4 pointsize 0.1
