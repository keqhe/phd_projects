set terminal postscript eps enhanced color 'Roman,30';
set size ratio 0.625
set output "bcm_burst_size_effects_incr.eps"
#set ylabel "CDF";
set ylabel "completion time (ms)";
set xlabel "burst size"
#set logscale x
#set logscale y
set xrange [0:750];
set yrange [0:40000];


#set xtics ("200" 200, "400" 400, "600" 600, "800" 800, "1000" 1000)

set key top right
#set key horizontal bottom
plot "bcm_burst_size_effects.txt" using 1:2:5 title "" with yerrorbars 

