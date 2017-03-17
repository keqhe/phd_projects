# Note you need gnuplot 4.4 for the pdfcairo terminal.

#set terminal pdfcairo font "Gill Sans,9" linewidth 4 rounded
#set terminal pdf enhanced color 'Roman,30'  linewidth 2 rounded
set terminal pdf font "Gill Sans,19" enhanced size 5,4

# Line style for axes
set style line 80 lt rgb "#808080"

# Line style for grid
set style line 81 lt 0  # dashed
set style line 81 lt rgb "#808080"  # grey

set grid back linestyle 81
#set border 3 back linestyle 80 # Remove border on top and right.  These
             # borders are useless and make it harder
             # to see plotted lines near the border.
# Also, put it in grey; no need for so much emphasis on a border.

set xtics nomirror
set ytics nomirror

#set log x
#set mxtics 10    # Makes logscale look good.

# Line styles: try to pick pleasing colors, rather
# than strictly primary colors or hard-to-see colors
# like gnuplot's default yellow.  Make the lines thick
# so they're easy to see in small plots in papers.
set style line 1 lt rgb "#A00000" lw 2 pt 1
set style line 2 lt rgb "#00A000" lw 2 pt 6
set style line 3 lt rgb "#5060D0" lw 2 pt 2
set style line 4 lt rgb "#F25900" lw 2 pt 9
set style line 5 lt rgb "#000000" lw 2 pt 14

set style line 1 lt rgb "#1b9e77" lw 10 pt 1
set style line 2 lt rgb "#d95f02" lw 10 pt 6
set style line 3 lt rgb "#7570b3" lw 10 pt 2
set style line 4 lt rgb "#e7298a" lw 10 pt 9
set style line 5 lt rgb "#636363" lw 10 pt 12

set output "tcp_flowcontrolOFF_convergence_tuningOFF.pdf"

set ylabel "Tput (Gbps)" offset 1
set xlabel "Time (seconds)"

#set key bottom right
set key top center 

#set xtics nomirror rotate by -45
#set xrange [0:15000]
#set yrange [50:80]
#set rmargin 5
#set xtics (1,2,3,4,5,6,7,8,9,10,16, 32, 64, 128, 256)

plot "dcn8-dcn19_tput.dat"  title "Flow 1" w l ls 1 linewidth 5, \
"dcn16-dcn20_tput.dat"  title "Flow 2" w l ls 2 linewidth 5 , \
"dcn5-dcn7_tput.dat"  title "Flow 3" w l ls 3 linewidth 5 , \
"dcn9-dcn14_tput.dat"  title "Flow 4" w l ls 4 linewidth 5, \
"dcn15-dcn17_tput.dat"  title "Flow 5" w l ls 5 linewidth 5
