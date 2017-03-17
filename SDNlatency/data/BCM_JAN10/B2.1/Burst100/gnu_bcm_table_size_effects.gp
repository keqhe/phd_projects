set terminal postscript eps enhanced color 'Roman,30';
set size ratio 0.625
set output "bcm_table_size_effects_B100.eps"
#set ylabel "CDF";
set ylabel "completion time (ms)";
set xlabel "table occupancy"
#set logscale x
#set logscale y
set xrange [0:650];
set yrange [0:500];


#set xtics ("200" 200, "400" 400, "600" 600, "800" 800, "1000" 1000)

set key top right
#set key horizontal bottom
plot "bcm_table_size_effects.txt" using 1:2:5 title "" with yerrorbars 

