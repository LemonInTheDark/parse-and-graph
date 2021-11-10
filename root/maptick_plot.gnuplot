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
outputfile5 = sprintf("%s Average by Server%s", filename, outputformat)

filename = "Pop"
filename = sprintf("%s%s", outputfolder, filename)
outputfile6 = sprintf("%s%s", filename, outputformat)
outputfile7 = sprintf("%s By Map%s", filename, outputformat)
outputfile8 = sprintf("%s By Server%s", filename, outputformat)


filename = "TD"
filename = sprintf("%s%s", outputfolder, filename)
outputfile9 = sprintf("%s Average%s", filename, outputformat)
outputfile10 = sprintf("%s Average By Map%s", filename, outputformat)
outputfile11 = sprintf("%s Average By Server%s", filename, outputformat)
outputfile12 = sprintf("%s%s", filename, outputformat)

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
mapfiles = "\"Delta Station.csv\" \"Ice Box Station.csv\" \"Kilo Station.csv\" \"MetaStation.csv\" \"PubbyStation.csv\" \"Tramstation.csv\""
serverfiles = "manuel.csv basil.csv sybil.csv terry.csv"
#files = system('dir /B *Station.csv') #GOD DAMN IT WINDOWS GIVE ME REGEX AHHHHHHHHHHHHHHHHHHHH

set output outputfile4
set title "Average Maptick Over Player Count By Map"
plot for [file in mapfiles] sprintf("%s%s", inputfolder, file) using 1:7 with lines title file 

set output outputfile5
set title "Average Maptick Over Player Count By Server"
plot for [file in serverfiles] sprintf("%s%s", inputfolder, file) using 1:7 with lines title file 

set ylabel 'Player Count'

set output outputfile6
set title "Average Player Count"
plot inputfile using 1:15 with lines

set output outputfile7
set title "Average Player Count By Map"
plot for [file in mapfiles] sprintf("%s%s", inputfolder, file) using 1:15 with lines title file

set output outputfile8
set title "Average Player Count By Server"
plot for [file in serverfiles] sprintf("%s%s", inputfolder, file) using 1:15 with lines title file

set ylabel 'TD'

set output outputfile9
set title "Average TD"
plot inputfile using 1:16 with lines

set output outputfile10
set title "Average TD By Map"
plot for [file in mapfiles] sprintf("%s%s", inputfolder, file) using 1:16 with lines title file

set output outputfile11
set title "Average TD By Server"
plot for [file in serverfiles] sprintf("%s%s", inputfolder, file) using 1:16 with lines title file

set output outputfile12
set title "TD"
plot inputfile using 1:5 with lines title "TD"