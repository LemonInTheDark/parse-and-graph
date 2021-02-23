set datafile separator ','
set terminal png
filename = "maptick"
inputfile = sprintf("%s%s", filename, ".csv")
outputformat = ".png"
outputfile1 = sprintf("%s1%s", filename, outputformat)
outputfile2 = sprintf("%s2%s", filename, outputformat)
outputfile3 = sprintf("%s3%s", filename, outputformat)
outputfile4 = sprintf("%s4%s", filename, outputformat)

set title "Deep Profiling"
set key autotitle columnheader 
set key noenhanced

set key at screen 1, graph 1

set rmargin 13
set output outputfile1
set title "Average Maptick by Round"
plot inputfile using 1:2 with lines

set rmargin 22
set output outputfile2
set title "Average Maptick Over Player Count By Round"
plot inputfile using 1:3 with lines

#I hate this fuck you admin team
files = "Delta%20Station.csv Ice%20Box%20Station.csv Kilo%20Station.csv MetaStation.csv PubbyStation.csv"
#files = system('dir /B *Station.csv') #GOD DAMN IT WINDOWS GIVE ME REGEX AHHHHHHHHHHHHHHHHHHHH

set rmargin 22
set output outputfile3
set title "Average Maptick Over Player Count By Map By Round"
plot for [file in files] file using 1:3 with lines title file

set rmargin 22
set output outputfile4
set title "Average Player Count By Map By Round"
plot for [file in files] file using 1:6 with lines title file