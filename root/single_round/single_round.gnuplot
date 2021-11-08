set datafile separator ','
set terminal png 

outputformat = ".png"

# so you can override them if you'd like
if(!exists("inputfilename")) inputfilename = "temporary"
if(!exists("inputfile")) inputfile = sprintf("%s%s", inputfilename, ".csv")
if(!exists("foldername")) foldername = sprintf("%u", time(0))

command = "mkdir ".foldername
system command

if(!exists("outputfilename")) outputfilename = "maptick"

filename = sprintf("%s/%s", foldername, outputfilename)

outputfile1 = sprintf("%s1%s", filename, outputformat)
outputfile2 = sprintf("%s2%s", filename, outputformat)
outputfile3 = sprintf("%s3%s", filename, outputformat)
outputfile4 = sprintf("%s4%s", filename, outputformat)
outputfile5 = sprintf("%s5%s", filename, outputformat)
outputfile6 = sprintf("%s6%s", filename, outputformat)
outputfile7 = sprintf("%s7%s", filename, outputformat)
outputfile8 = sprintf("%s8%s", filename, outputformat)
outputfile9 = sprintf("%s9%s", filename, outputformat)
outputfile10 = sprintf("%s10%s", filename, outputformat)

set title "Deep Profiling"
set key autotitle columnheader 
set key noenhanced
set autoscale fix

set xlabel 'World Time'
set ylabel 'Maptick Stats'

set key at screen 1, graph 1
set rmargin 13

set output outputfile1
set title "Classic Stats"
plot inputfile using 1:3 with lines, '' using 1:4 with lines, '' using 1:2 with lines

set term png size 1150, 600 
set size ratio 0.85

set ylabel 'Change Per Second'

set output outputfile2
set title "Complex Shit 1"
plot inputfile using 1:28 with lines, '' using 1:29 with lines, '' using 1:30 with lines, '' using 1:31 with lines, '' using 1:32 with lines, '' using 1:33 with lines, '' using 1:34 with lines, '' using 1:35 with lines, '' using 1:36 with lines, '' using 1:37 with lines, '' using 1:38 with lines, '' using 1:39 with lines, '' using 1:40 with lines, '' using 1:41 with lines, '' using 1:42 with lines, '' using 1:43 with lines, '' using 1:44 with lines, '' using 1:45 with lines, '' using 1:46 with lines, '' using 1:47 with lines, '' using 1:48 with lines, '' using 1:49 with lines

set output outputfile3
set title "Complex Shit 2"
plot inputfile using 1:28 with lines, '' using 1:34 with lines, '' using 1:35 with lines, '' using 1:36 with lines, '' using 1:37 with lines, '' using 1:38 with lines

set output outputfile4
set title "Complex Shit 3"
plot inputfile using 1:28 with lines, '' using 1:39 with lines, '' using 1:40 with lines, '' using 1:41 with lines, '' using 1:42 with lines, '' using 1:43 with lines

set output outputfile5
set title "Complex Shit 4"
plot inputfile using 1:28 with lines, '' using 1:44 with lines, '' using 1:45 with lines, '' using 1:46 with lines, '' using 1:47 with lines, '' using 1:48 with lines

set output outputfile6
set title "Complex Shit 5"
plot inputfile using 1:28 with lines, '' using 1:49 with lines
command = "cd .."
system command
