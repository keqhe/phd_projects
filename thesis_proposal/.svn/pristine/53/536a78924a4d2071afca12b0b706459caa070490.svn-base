# Note you need gnuplot 4.4 for the pdfcairo terminal.

set terminal pdfcairo font "Gill Sans,18" linewidth 4 rounded

#set size ratio 0.35

set output '2flows-ts.pdf'

# Line style for axes
set style line 80 lt rgb "#808080"

# Line style for grid
set style line 81 lt 0  # dashed
set style line 81 lt rgb "#808080"  # grey

set grid back linestyle 81
set border 3 back linestyle 80 # Remove border on top and right.  These
             # borders are useless and make it harder
             # to see plotted lines near the border.
    # Also, put it in grey; no need for so much emphasis on a border.
#set xtics nomirror 0,10000,50000

set arrow from 11,0 to 11,9000 nohead
set xlabel "Time (s)"
set ylabel "Throughput (Gbps)"
plot 'flow1.data' w lp, 'flow2.data' w lp
