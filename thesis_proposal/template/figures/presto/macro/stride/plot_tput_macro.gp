#set terminal pdf enhanced
set terminal pdf font "Gill Sans,18" enhanced

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
set ylabel "Avg Flow Tput (Gbps)" offset 2

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

set output "macro_compare_tput_witherrbar.pdf"

set boxwidth 1 absolute
set style fill solid border rgb "black"
set style data histogram
#set style histogram cluster gap 2
set style histogram errorbars gap 0 lw 2

set ytics 1
set yrange [0:10]
set xlabel "Workloads"


set style histogram errorbars gap 2 lw 1
#set key horizontal outside
set key top left
#set key autotitle columnheader

#without errorbar
#plot 'scalability_compare_tput_bar_only.dat' using 2 t "ECMP(theory)",'' using 3 t "ECMP", '' using 4  t "Presto", '' using 5:xtic(1)  t "N-block"

plot 'macro_tput_errorbar.dat' using ($2/1000):($3/1000):($4/1000):xtic(1) t "ECMP" w hist ls 1 fs pattern 1, '' using ($5/1000):($6/1000):($7/1000) t "MPTCP" w hist ls 2 fs pattern 2, '' using ($8/1000):($9/1000):($10/1000) t "Presto" w hist ls 3 fs pattern 3, '' using ($11/1000):($12/1000):($13/1000)  t "Optimal" w hist ls 4 fs pattern 9
 
#newhistogram "8", 'scalability_compare_tput_errorbar_path8.dat' using 2:3:4 t "ECMP(sim)" w hist ls 1, \
# '' using 5:6:7 t "ECMP" w hist ls 2, \
# '' using 11:12:13  t "MPTCP" w hist ls 3, \
# '' using 8:9:10  t "Presto" w hist ls 4, \
# '' using 14:15:16:xtic(1)  t "Optimal" w hist ls 5 
