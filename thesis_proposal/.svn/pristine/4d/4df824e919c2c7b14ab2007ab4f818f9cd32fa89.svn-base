# Note you need gnuplot 4.4 for the pdfcairo terminal.

#set terminal pdfcairo font "Gill Sans,9" linewidth 4 rounded
#set terminal postscript eps enhanced color 'Roman,30'  linewidth 2 rounded

set terminal pdfcairo font "Gill Sans,29" enhanced size 5,4

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

set style line 1 lt rgb "#1b9e77" lw 5 pt 1
set style line 2 lt rgb "#d95f02" lw 5 pt 6
set style line 3 lt rgb "#7570b3" lw 5 pt 2
set style line 4 lt rgb "#e7298a" lw 5 pt 9
set style line 5 lt rgb "#636363" lw 5 pt 12

set output "metric1_seg_cdf_compare.pdf"

set ylabel "CDF" offset 2
set xlabel "Out-of-Order Segment Count"

set key bottom right

#set xtics nomirror rotate by -45
#set xrange [37503:48443]
#set yrange [0:50]

#plot "chunk_seg.txt" using 1:2 title "" w lp ls 1 linewidth 4 pointsize 2
plot "dcn16_without/chunk_seg.txt.cdf" using 1:2 title "Official GRO" w lp ls 1 pointsize 3,\
"dcn16_with/chunk_seg.txt.cdf" using 1:2 title "Presto GRO" w lp ls 2 pointsize 3
