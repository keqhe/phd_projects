set term post eps color solid enh "Times-Roman" 16

set output "proxyCPU.eps"
input = 'proxyCPU.dat'

lwi = 10

set xlabel 'flow arrival rate (in 1000s)' font "Times-Roman,35"
set xtics font "Times-Roman,25"
set ylabel 'peak %CPU util' font "Times-Roman,35"
set ytics font "Times-Roman,25"
set xrange [0:80]

set size 0.8,0.6

set pointsize 2
set grid

plot input using ($1/1000):($2) title "" with linespoints lw lwi

#set boxwidth 8000
#set style fill solid
#plot "data.dat" using ($1):($2) with boxes
