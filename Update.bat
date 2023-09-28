@ECHO OFF

PUSHD "%~dp0"
CD root

ECHO Grabbing Logs
py -3.6 RawLogsScraper.py

ECHO Averaging CSV files
py -3.6 MaptickAverager.py

ECHO Plotting Graphs
gnuplot maptick_plot.gnuplot

POPD "%~dp0"