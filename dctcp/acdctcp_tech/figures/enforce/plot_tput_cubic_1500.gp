# Note you need gnuplot 4.4 for the pdfcairo terminal.

#set terminal pdfcairo font "Gill Sans,9" linewidth 4 rounded
#set terminal pdf enhanced color 'Roman,30'  linewidth 2 rounded
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
set style line 5 lt rgb "#000000" lw 2 pt 14

set style line 1 lt rgb "#1b9e77" lw 10 pt 1
set style line 2 lt rgb "#d95f02" lw 10 pt 6
set style line 3 lt rgb "#7570b3" lw 10 pt 2
set style line 4 lt rgb "#e7298a" lw 10 pt 9
set style line 5 lt rgb "#636363" lw 10 pt 12

set output "tput_cwnd_rwnd_cubic_15k.pdf"

set ylabel "Throughput (Gbps)" offset 2
set xlabel "Maximal CWND (pkts)/RWND (MSS)"

set key bottom right

set xtics nomirror rotate by -45
set xrange [0:256]
#set yrange [1:256]
#set rmargin 5
#set xtics (1,2,3,4,5,6,7,8,9,10,16, 32, 64, 128, 256)

plot "cwnd/cubic_cubic/tput_cwnd_1500.dat"  using 1:($2/1000) title "CWND" w lp ls 1 linewidth 8 pointsize 2, \
"rwnd/cubic_cubic/tput_rwnd_1500_add.dat"  using 1:($2/1000) title "RWND" w lp ls 2 linewidth 8 pointsize 2
