#!/bin/sh
@echo off
echo Grabbing Logs
RawLogsScraper.py
echo Averaging CSV files
MaptickAverager.py
echo Plotting Graphs
cd maptick
gnuplot maptick_plot.gnuplot