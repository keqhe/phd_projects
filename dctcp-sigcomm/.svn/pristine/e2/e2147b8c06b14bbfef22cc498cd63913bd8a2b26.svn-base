#set terminal pdf enhanced
set terminal pdf font "Gill Sans,17" enhanced 

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
set xlabel "Experiments (with different β combinations)"

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

set output "qos_stacked.pdf"

set boxwidth 0.5 absolute
set style fill solid border rgb "black"
set style data histogram
set style histogram rowstacked gap 2 

#set ytics 5
#set logscale y 
set yrange [0:10]


set key outside top right horizontal
set xtics nomirror rotate by -20

plot 'qos_stacked.dat' using ($2/1000):xtic(1) title "F1" w hist ls 1 fs pattern 1, '' using ($3/1000) title "F2" w hist ls 1 fs pattern 2, '' using ($4/1000) title "F3" w hist ls 1 fs pattern 3, '' using ($5/1000) title "F4" w hist ls 1 fs pattern 4, '' using ($6/1000) title "F5" w hist ls 1 fs pattern 5 
