# Maptick scraper/parsing tool

This is a set of tools developed to aid in the tracking of maptick for the /tg/station server.

It scrapes all available performance logs, processes them into csv files (One for each map, and one global one), and then uses `gnuplot` to plot them in a few different ways I've judged as useful.

## Scraping

We don't scrape all performance logs, since some of them from before 2020/11/11 don't scrape well and don't match the current system.
Uh if you stop the scraper midway it will just forget about those files, so... don't do that.

## Parsing

A brief note on parsing, we store each round as one data-point, alongside the avg maptick and player count across it, and the maptick per player. 

We also compute a running average of maptick per player and player count, to make graphing cleaner.

## Updating your data

Running `Update.bat` will pull all the logs you don't have (Outside some edgecases I don't have the brainpower to fix, read the python file) parse them into csv files, and generate a new plot from them.

## Single Round Parsing

If you'd like to graph a single round you've already pulled, use `GraphOne.bat`. If you'd like to learn more about any of this feel free to read [root/README.md](root/README.md)

## Dependencies

This project was created with `python 3.6`, you'll need at least `python 3` for the logs parser to run properly.
Additionally you will need gnuplot installed, with a version above 5. This is to support graphing several files onto one graph.

## License

This codebase is licensed under GNU GPLv3. See [LICENSE](LICENSE) for more details.