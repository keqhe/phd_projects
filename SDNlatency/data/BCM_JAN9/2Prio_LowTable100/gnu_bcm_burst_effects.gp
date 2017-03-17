set terminal postscript eps enhanced color 'Roman,30';
set size ratio 0.625
set output "bcm_two_pri_low_100_low_burstB.eps"
#set ylabel "CDF";
set ylabel "completion time (ms)";
set xlabel "burst size"
#set logscale x
#set logscale y
set xrange [0:650];
set yrange [0:20000];


#set xtics ("200" 200, "400" 400, "600" 600, "800" 800, "1000" 1000)

set key top right
#set key horizontal bottom
plot "bcm_burst_size_effects.txt" using 1:2:5 title "" with yerrorbars 

