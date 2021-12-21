# Maptick scraper/parsing tool

This is a set of tools developed to aid in the tracking of maptick, td, and pop for the /tg/station server.

It scrapes all available performance logs, processes them into csv files (One for each map, one for each server, and a few global ones), and then uses `gnuplot` to plot them in a few different ways I've judged as useful.

## Scraping

We don't scrape all performance logs, since some of them from before 2020/11/11 don't scrape well and don't match the current system.

## Parsing

A brief note on parsing, we compile each round into one data-point, attached to some other info about it.

## Updating your data

Running `Update.bat` will pull all the logs you don't have (Outside some edgecases I don't have the brainpower to fix, read the python file) parse them into csv files, and generate a new plot from them.

## Single Round Parsing

If you'd like to graph a single round you've already pulled, use `GraphOne.bat`. It'll dump images for that round into [root/single_round](root/single_round)

## More Information 

If you'd like to learn more about any of this go read [root/README.md](root/README.md), it goes into more detail about how things work and how to interact with them

## Dependencies

This project was created with `python 3.6`, you'll need at least `python 3` for the logs parser to run properly.

Additionally you will need gnuplot installed, with a version above 5. This is to support graphing several files onto one graph. Needs to be in your path too, because I'm a moron. [Have another Link](http://www.gnuplot.info/)

## License

This codebase is licensed under GNU GPLv3. See [LICENSE](LICENSE) for more details.