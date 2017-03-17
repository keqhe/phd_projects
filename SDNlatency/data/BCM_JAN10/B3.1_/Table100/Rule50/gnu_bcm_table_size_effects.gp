set terminal postscript eps enhanced color 'Roman,30';
set size ratio 0.625
set output "bcm_insertion_rate_effects_table100_rule500.eps"
#set ylabel "CDF";
set ylabel "average insertion delay (ms)";
set xlabel "insertion rate (rule/s)"
#set logscale x
#set logscale y
set xrange [0:450];
set yrange [0:150];


set xtics ("100" 100, "200" 200, "300" 300, "400" 400)

set key top right
#set key horizontal bottom
plot "bcm_insertion_rate_effects.txt" using 1:2:5 title "" with yerrorbars  

