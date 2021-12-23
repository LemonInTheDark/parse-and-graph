#!/bin/sh

@echo off
pushd "%~dp0"
cd root
echo Grabbing Logs
py RawLogsScraper.py
echo Averaging CSV files
py MaptickAverager.py
echo Plotting Graphs
gnuplot maptick_plot.gnuplot
popd "%~dp0"
pause
