set datafile separator ','
set terminal png 

outputformat = ".png"

# so you can override them if you'd like
if(!exists("inputfilename")) inputfilename = "temporary"
if(!exists("inputfile")) inputfile = sprintf("%s%s", inputfilename, ".csv")
if(!exists("foldername")) foldername = sprintf("%u", time(0))

command = "mkdir ".foldername
system command

if(!exists("outputfilename")) outputfilename = "Sendmaps "

filename = sprintf("%s/%s", foldername, outputfilename)

outputfile1 = sprintf("%s/Classic Stats%s", foldername, outputformat)
outputfile2 = sprintf("%sEverything%s", filename, outputformat)
outputfile3 = sprintf("%sGlobal%s", filename, outputformat)
outputfile4 = sprintf("%sPer Client%s", filename, outputformat)
outputfile5 = sprintf("%sMap Data%s", filename, outputformat)
outputfile6 = sprintf("%sMovable Changes%s", filename, outputformat)
outputfile7 = sprintf("%sAtmos%s", filename, outputformat)

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
set title "Everything SendMaps"
plot inputfile using 1:32 with lines, '' using 1:33 with lines, '' using 1:34 with lines, '' using 1:35 with lines, '' using 1:36 with lines, '' using 1:37 with lines, '' using 1:38 with lines, '' using 1:39 with lines, '' using 1:40 with lines, '' using 1:41 with lines, '' using 1:42 with lines, '' using 1:43 with lines, '' using 1:44 with lines, '' using 1:45 with lines, '' using 1:46 with lines, '' using 1:47 with lines, '' using 1:48 with lines, '' using 1:49 with lines, '' using 1:50 with lines, '' using 1:51 with lines, '' using 1:52 with lines, '' using 1:53 with lines

set output outputfile3
set title "SendMaps Global"
plot inputfile using 1:32 with lines, '' using 1:34 with lines, '' using 1:35 with lines, '' using 1:36 with lines

set output outputfile4
set title "SendMaps Per Client"
plot inputfile using 1:36 with lines, '' using 1:37 with lines, '' using 1:38 with lines, '' using 1:39 with lines, '' using 1:40 with lines

set output outputfile5
set title "SendMaps Map Data"
plot inputfile using 1:40 with lines, '' using 1:41 with lines, '' using 1:42 with lines, '' using 1:43 with lines, '' using 1:44 with lines, '' using 1:45 with lines, '' using 1:46 with lines, '' using 1:47 with lines, '' using 1:48 with lines, '' using 1:49 with lines, '' using 1:50 with lines

set output outputfile6
set title "SendMaps Movable Changes"
plot inputfile using 1:52 with lines, '' using 1:51 with lines, '' using 1:52 with lines, '' using 1:53 with lines

set output outputfile7
set title "Atmos Subprocesses"
plot inputfile using 1:6 with lines, '' using 1:7 with lines, '' using 1:8 with lines
