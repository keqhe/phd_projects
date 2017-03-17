set terminal postscript eps enhanced color 'Roman,30';
set size ratio 0.625
set output "same_priority_bcm_simple.eps"
#set ylabel "CDF";
set ylabel "latency (ms)";
set xlabel "openflow rule #"
#set logscale x
set logscale y
set xrange [1:768];
set yrange [0.1:5000];


#set xtics ("10" 20, "20" 40, "30" 60, "40" 80, "50" 100, "60" 120, "70" 140)

#set key top right
set key horizontal bottom
plot "same_priority_bcm.txt" using 1:2 title "10" with linespoints linetype 1 linecolor 3 linewidth 3 pointtype 1 pointsize 0.1, \
"same_priority_bcm.txt" using 1:4 title "50" with linespoints linetype 1 linecolor 4 linewidth 3 pointtype 3 pointsize 0.1,\
"same_priority_bcm.txt" using 1:5 title "100" with linespoints linetype 1 linecolor 5 linewidth 3 pointtype 4 pointsize 0.1,\
"same_priority_bcm.txt" using 1:6 title "150" with linespoints linetype 1 linecolor 7 linewidth 3 pointtype 5 pointsize 0.1,\
"same_priority_bcm.txt" using 1:7 title "200" with linespoints linetype 1 linecolor 9 linewidth 3 pointtype 6 pointsize 0.1,\
"same_priority_bcm.txt" using 1:10 title "500" with linespoints linetype 1 linecolor 10 linewidth 3 pointtype 9 pointsize 0.1
