#set terminal pdf enhanced
set terminal pdf font "Gill Sans,16" enhanced

# Line style for axes
set style line 80 lt rgb "#808080"

# Line style for grid
set style line 81 lt 0  # dashed
set style line 81 lt rgb "#808080"  # grey

#set grid back linestyle 81

#set border 3 back linestyle 80 # Remove border on top and right.  These
             # borders are useless and make it harder
             # to see plotted lines near the border.
# Also, put it in grey; no need for so much emphasis on a border.

set xtics nomirror
set ytics nomirror

set auto x
set ylabel "Tput (Gbps)" offset 2

# Line styles: try to pick pleasing colors, rather
# than strictly primary colors or hard-to-see colors
# like gnuplot's default yellow.  Make the lines thick
# so they're easy to see in small plots in papers.
#set style line 1 lt rgb "#CCCCCC" lw 2 pt 1
#set style line 2 lt rgb "#999999" lw 2 pt 1
#set style line 3 lt rgb "#666666" lw 2 pt 1
#set style line 4 lt rgb "#333333" lw 2 pt 1
#set style line 5 lt rgb "#000000" lw 2 pt 1

set style line 1 lt rgb "#A00000" lw 2 pt 1
set style line 2 lt rgb "#00A000" lw 2 pt 6
set style line 3 lt rgb "#5060D0" lw 2 pt 2
set style line 4 lt rgb "#F25900" lw 2 pt 9
set style line 5 lt rgb "#636363" lw 2 pt 12

set style line 1 lt rgb "#1b9e77" lw 2 pt 1
set style line 2 lt rgb "#d95f02" lw 2 pt 6
set style line 3 lt rgb "#7570b3" lw 2 pt 2
set style line 4 lt rgb "#e7298a" lw 2 pt 9
set style line 5 lt rgb "#636363" lw 2 pt 12

set output "qos_0.75_0.75_0.5_0.5_0.25.pdf"

set boxwidth 1 absolute
set style fill solid border rgb "black"
set style data histogram
set style histogram cluster gap 1
#set style histogram errorbars gap 0 lw 2

#set ytics 5
#set logscale y 
set yrange [0:4]
#set xtics ("0.5" 0, "0.5" 1, "0.5" 2, "0.5" 3, "0.5" 4)
#set xtics ("0.5" 0, "0.5" 1, "0.25" 2, "0.25" 3, "0.25" 4)
set xtics ("0.75" 0, "0.75" 1, "0.5" 2, "0.5" 3, "0.25" 4)
set xlabel "Beta"


set style histogram clustered
#set key horizontal outside
set key top left
#set key autotitle columnheader

plot 'qos_two_0.75_two_0.5_one_0.25.dat' using ($2/1000) t "" w hist ls 1 fs pattern 1
 
