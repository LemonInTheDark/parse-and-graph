set datafile separator ','
set terminal png
outputformat = ".png"
inputfolder = "compiled/" 
outputfolder = "images/"

filename = "Maptick"
filename = sprintf("%s%s", outputfolder, filename)
inputfile = sprintf("%s%s%s", inputfolder, "maptick", ".csv")

outputfile1 = sprintf("%s Highpass%s", filename, outputformat)
outputfile2 = sprintf("%s%s", filename, outputformat)
outputfile3 = sprintf("%s Average%s", filename, outputformat)
outputfile4 = sprintf("%s Average By Map%s", filename, outputformat)

filename = "Pop"
filename = sprintf("%s%s", outputfolder, filename)
outputfile5 = sprintf("%s%s", filename, outputformat)
outputfile6 = sprintf("%s By Map%s", filename, outputformat)

filename = "TD"
filename = sprintf("%s%s", outputfolder, filename)
outputfile7 = sprintf("%s Average%s", filename, outputformat)
outputfile8 = sprintf("%s Average By Map%s", filename, outputformat)
outputfile9 = sprintf("%s%s", filename, outputformat)
outputfile10 = sprintf("%s By Map%s", filename, outputformat)
outputfile11 = sprintf("%s Over Pop%s", filename, outputformat)
outputfile12 = sprintf("%s Ober Pop By Map%s", filename, outputformat)

set key autotitle columnheader 
set key noenhanced
set term png size 1000, 600 
set size ratio 0.85

set key at screen 1, graph 1
set xlabel 'Round Count'
set ylabel 'Maptick Per Person'
set xtics rotate by -40
set yrange [0:]
set grid ytics

#CSV file is formatted like this
# id, maptick_to_player, maptick, players, td, td_to_player
# followed by three entries for everything but the id. avg, min, and max

#To find the index of the header you want, use this forumula
# 6 + ((spot in list - 2) * 3) + (spot in list - 1) * header you want

highpass = "highpass_maptick.csv"
highpass = sprintf("%s%s", inputfolder, highpass)

set rmargin 13
set output outputfile1
set title "MPP (High Pass Filter)"
plot highpass using 1:2 with lines title "Maptick Per Player"

set rmargin 13
set output outputfile2
set title "MPP"
plot inputfile using 1:2 with lines title "Maptick Per Player"

set rmargin 22
set output outputfile3
set title "Average Maptick Over Player Count"
plot highpass using 1:7 with lines title "Maptick Per Player", "labels.csv" using 2:3:1 with labels title ""

#I hate this fuck you admin team
files = "Delta%20Station.csv Ice%20Box%20Station.csv Kilo%20Station.csv MetaStation.csv PubbyStation.csv Tramstation.csv"
#files = system('dir /B *Station.csv') #GOD DAMN IT WINDOWS GIVE ME REGEX AHHHHHHHHHHHHHHHHHHHH

set output outputfile4
set title "Average Maptick Over Player Count By Map"
plot for [file in files] sprintf("%s%s", inputfolder, file) using 1:7 with lines title file 

set ylabel 'Player Count'

set output outputfile5
set title "Average Player Count"
plot inputfile using 1:15 with lines

set output outputfile6
set title "Average Player Count By Map"
plot for [file in files] sprintf("%s%s", inputfolder, file) using 1:15 with lines title file

set ylabel 'TD'

set output outputfile7
set title "Average TD"
plot inputfile using 1:16 with lines

set output outputfile8
set title "Average TD By Map"
plot for [file in files] sprintf("%s%s", inputfolder, file) using 1:16 with lines title file

set output outputfile9
set title "TD"
plot inputfile using 1:5 with lines title "TD"

set output outputfile10
set title "TD By Map"
plot for [file in files] sprintf("%s%s", inputfolder, file) using 1:5 with lines title file

set ylabel 'TD Per Person'

set output outputfile11
set title "TD Over Players"
plot inputfile using 1:6 with lines title "TD Over Pop"

set output outputfile12
set title "TD By Players By Map"
plot for [file in files] sprintf("%s%s", inputfolder, file) using 1:6 with lines title file
