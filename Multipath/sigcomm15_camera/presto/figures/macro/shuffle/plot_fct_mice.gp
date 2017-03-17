# Note you need gnuplot 4.4 for the pdfcairo terminal.

#set terminal pdfcairo font "Gill Sans,9" linewidth 4 rounded
#set terminal pdf enhanced color 'Roman,30'  linewidth 2 rounded
set terminal pdf font "Gill Sans,24" enhanced size 5,4

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

set style line 1 lt rgb "#1b9e77" lw 12 pt 1
set style line 2 lt rgb "#d95f02" lw 12 pt 6
set style line 3 lt rgb "#7570b3" lw 12 pt 2
set style line 4 lt rgb "#e7298a" lw 12 pt 9
set style line 5 lt rgb "#636363" lw 12 pt 12

set output "macro_compare_fct_shuffle_mice.pdf"

set ylabel "CDF" offset 2
set xlabel "Flow Completion Time (milliseconds)"

set key bottom right
set xtics 5
#set xtics nomirror rotate by -45
set xrange [0:20]
set yrange [0:0.999]
#set rmargin 5

plot "ecmp.mice.fct.cdf" using ($1/1000):2  title "ECMP" w lp ls 1 pointinterval 500 pointsize 2,\
"mptcp.mice.fct.cdf" using ($1/1000):2 title "MPTCP" w lp ls 2 pointinterval 600 pointsize 2, \
"presto.mice.fct.cdf"  using ($1/1000):2 title "Presto" w lp ls 3 pointinterval 800 pointsize 2, \
"optimal.mice.fct.cdf"  using ($1/1000):2 title "Optimal" w lp ls 4 pointinterval 800 pointsize 2
#"OnePara_64KB_Delta55/ping.txt.cdf"  title "64K,55us" w lp ls 3 linewidth 4 pointsize 2, \
#"OnePara_64KB_Delta215/ping.txt.cdf"  title "64K,215us" w lp ls 4 linewidth 4 pointsize 2
#"ecmp_tput.cdf"  title "ecmp" w lp ls 5 linewidth 4 pointsize 2
#plot "chunk_seg.txt" using 1:2 title "" w points pointsize 1
