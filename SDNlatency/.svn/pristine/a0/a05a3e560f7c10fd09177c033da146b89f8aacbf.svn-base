set terminal postscript eps enhanced color 'Roman,30';
set size ratio 0.625
set output "MB_perf_HP.eps"
#set ylabel "CDF";
set ylabel "CDF";
set xlabel "Inbound delay (ms)"
set logscale x
#set logscale y
set xrange [0.001:5];
set yrange [0:1];


#set xtics ("200" 200, "400" 400, "600" 600, "800" 800, "1000" 1000)

set key bottom right
#set key horizontal bottom
plot "myCDF_500.txt" using 1:2 title "flow rate = 500/s" with  linespoints linetype 1 linecolor 3 linewidth 3 pointtype 1 pointsize 1,\
"myCDF_1000.txt" using 1:2 title "flow rate = 1000/s" with  linespoints linetype 2 linecolor 5 linewidth 3 pointtype 1 pointsize 1, \
"myCDF_2000_.txt" using 1:2 title "flow rate = 2000/s" with  linespoints linetype 3 linecolor 7 linewidth 3 pointtype 1 pointsize 1
