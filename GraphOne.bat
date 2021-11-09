#!/bin/sh

@echo off
pushd "%~dp0"
cd root
echo Parsing file
py SingleROUND.py
echo Plotting Graphs
cd single_round
gnuplot single_round.gnuplot
popd