#http://www.codealias.info/technotes/gnuplot_rowstacked_histogram_example
#may also want to check:
#  http://stackoverflow.com/questions/23406222/put-histogram-side-by-side
#set terminal pdf

# want to get all of them, but not working. made some headway here, 
#also look at: http://psy.swansea.ac.uk/staff/carter/gnuplot/gnuplot_histograms.htm

set terminal pdf font "Gill Sans,19" 
set output "histo.pdf"

set boxwidth 0.75 absolute
set style fill solid 1.00 border -1
set style histogram rowstacked
set style data histograms
set xtics 1000 nomirror
set ytics 100 nomirror
set mxtics 2
set mytics 2
set ytics 100
set yrange [0:1000]
set ylabel "Flowlet Size (MB)" offset 2
set xlabel "Competing Flows"
set nokey

plot 'scp.data' using 2 t "Server" fs pattern 1, '' using 3 t "Client" fs pattern 2, '' u 4 fs pattern 3, '' u 5 fs pattern 4, '' u 6 fs pattern 5, '' using 7:xtic(1) t "Network" fs pattern 6, '' u 8 fs pattern 7, '' u 9 fs pattern 8, '' u 10 fs pattern 9, '' u 11 fs pattern 10
#  '' u 11, '' u 12, '' u 13, '' u 14

#plot 'scp.data' using 2:xtic(1), for [i=1:22] '' using i
#plot for [COL=2:4] 'scp.data' using COL:xticlabels(1) title columnheader


