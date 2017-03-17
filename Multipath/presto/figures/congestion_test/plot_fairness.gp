# Note you need gnuplot 4.4 for the pdfcairo terminal.

#set terminal pdfcairo font "Gill Sans,9" linewidth 4 rounded
#set terminal postscript eps enhanced color 'Roman,30'  linewidth 2 rounded
set terminal pdf font "Gill Sans,29" enhanced size 5,4

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
set style line 5 lt rgb "#8A2BE2" lw 2 pt 12
set style line 6 lt rgb "#DAA520" lw 2 pt 15

set style line 1 lt rgb "#1b9e77" lw 15 pt 1
set style line 2 lt rgb "#d95f02" lw 15 pt 6
set style line 3 lt rgb "#7570b3" lw 15 pt 2
set style line 4 lt rgb "#e7298a" lw 15 pt 9
set style line 5 lt rgb "#636363" lw 15 pt 12

set output "congestion_compare_fairness.pdf"

set ylabel "Fairness Index" offset 2
set xlabel "Oversubscription Ratio"

set key bottom left

#set xtics 1
#set xtics nomirror rotate by -45
#set xrange [37503:48443]
set yrange [0.5:1]

###use ejr jain metric
plot \
"fair_index.dat" using 1:5 title "ECMP" w lp ls 1 pointsize 2, \
"fair_index.dat" using 1:11 title "MPTCP" w lp ls 2 pointsize 2, \
"fair_index.dat" using 1:9 title "Presto" w lp ls 3 pointsize 2


###if you want to distinguish ejr and khe jain metric
#plot "fair_index.dat" using 1:2 title "ECMP" w lp ls 1 pointsize 3,\
#"fair_index.dat" using 1:3 title "Presto" w lp ls 2 pointsize 3, \
#"fair_index.dat" using 1:4 title "Optimal" w lp ls 5 pointsize 3, \
#"fair_index.dat" using 1:5 title "ECMP (ejr)" w lp ls 3 pointsize 3, \
#"fair_index.dat" using 1:6 title "Presto (ejr)" w lp ls 4 pointsize 3,\
#"fair_index.dat" using 1:7 title "Optimal (ejr)" w lp ls 6 pointsize 3
