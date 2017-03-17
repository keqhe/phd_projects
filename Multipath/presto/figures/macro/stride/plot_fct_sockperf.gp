# Note you need gnuplot 4.4 for the pdfcairo terminal.

#set terminal pdfcairo font "Gill Sans,9" linewidth 4 rounded
#set terminal pdf enhanced color 'Roman,30'  linewidth 2 rounded
set terminal pdf font "Gill Sans,17" enhanced

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

set output "macro_compare_fct_stride_sockperf.pdf"

set ylabel "CDF"
set xlabel "Flow Completion Time (microseconds)"

set key bottom right

set xtics nomirror rotate by -45
set xrange [0:10000]
#set yrange [0:10000]
set rmargin 5

plot "ecmp.sock.fct.cdf"  title "ECMP" w lp ls 1 linewidth 4 pointsize 1 ,\
"mptcp_low.sock.fct.cdf" title "MPTCP" w lp ls 2 linewidth 4 pointsize 1, \
"presto.sock.fct.cdf"  title "Presto" w lp ls 3 linewidth 4 pointsize 1, \
"optimal.sock.fct.cdf"  title "Optimal" w lp ls 4 linewidth 4 pointsize 1
#"OnePara_64KB_Delta55/ping.txt.cdf"  title "64K,55us" w lp ls 3 linewidth 4 pointsize 2, \
#"OnePara_64KB_Delta215/ping.txt.cdf"  title "64K,215us" w lp ls 4 linewidth 4 pointsize 2
#"ecmp_tput.cdf"  title "ecmp" w lp ls 5 linewidth 4 pointsize 2
#plot "chunk_seg.txt" using 1:2 title "" w points pointsize 1
