set terminal postscript eps enhanced color 'Roman,30';
set size ratio 0.625
set output "compare_complexity_bcm.eps"
#set ylabel "CDF";
set ylabel "latency (ms)";
set xlabel "proactive insertion rate (rules per sec)"
#set logscale x
#set logscale y
set xrange [1:700];
set yrange [0.1:2000];


#set xtics ("10" 20, "20" 40, "30" 60, "40" 80, "50" 100, "60" 120, "70" 140)

set key top right
#set key horizontal bottom
plot "bcm_avg.txt" using 1:2 title "simple" with linespoints linetype 1 linecolor 3 linewidth 3 pointtype 1 pointsize 0.1, \
"bcm_avg.txt" using 1:3 title "complex" with linespoints linetype 2 linecolor 4 linewidth 3 pointtype 3 pointsize 0.1
