set terminal postscript eps enhanced color 'Roman,30';
set size ratio 0.625
set output "bcm_polling_table0_burst100.eps"
#set ylabel "CDF";
set ylabel "completion time (ms)";
set xlabel "flow stats polling count"
#set logscale x
#set logscale y
set xrange [0:10];
set yrange [0:600];


#set xtics ("200" 200, "400" 400, "600" 600, "800" 800, "1000" 1000)

set key top right
#set key horizontal bottom
plot "bcm_polling_effects_table0_burst100.txt" using 1:2:5 title "" linepoints with yerrorbars 

