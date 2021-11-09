# What is all this?

## Main Graphing

### [RawLogsScraper](RawLogsScraper.py)

Not a whole lot to say here, this scrapes round and map information from the tgstation13.org public logs.
There's a list of servers to pull from if you'd like to futz around with it. We don't actually have support for graphing by round right now, I'll add that later maybe.

Oh right uh, mood.json exists. Create one and edit it to match your server creds if for some reason you want to pull from raw logs (Don't forget to change the url). Or just like, don't? I don't remember if you need to for public logs or not.

### [MaptickAverager](MaptickAverager.py)

This file's in charge of taking raw csv files and processing them. This includes a number of things
I'll be brief, but almost all aspects of this process are modifiable. Changing any of the following vars in the python code will lead to full recompiles to match your changes.

Oh on that note, we don't fully process our files all at once, because frankly I'm doing all this in python to prove a point to myself, so if we did it would be slow as balls. Information about the last compile is stored in [compiled/last_run.dat](compiled/last_run.dat), if you want to poke around, or just delete it to trigger a full recompile. Anyway.

- The size of our moving average: `movingbackward movingforward`
- The size of moving minimum and maximum ranges: `boundbackward boundforward` (currently not graphed, do it yourself)
- The round to start graphing at: `starting_at`
- The maptick threshold for ignoring rounds: `highpass_threshold` (exists so spikes don't fuck up graphing, you prob don't need to change this)

### [maptick_plot](maptick_plot.gnuplot)

This is the file in charge of taking the compiled files, and making them pretty. Futz around here if you want to change what info graphed, or how the graph looks.

If you'd like to change the positioning of the labels that show on the averaged graph, go to [labels.csv](labels.csv) 
[canonlabels.csv](labels.csv) exists as a reminder for where things ought to be when you're futzing around with stuff
Changing these values is going to be needed as time goes on and the span of our graph gets larger and larger. Speaking of which I'm pretty sure my current format will break if/when enough rounds happen. Should prob do something about that.

## Targeted Parsing

### [SingleRound](SingleRound.py)

This parses a single csv file for more detailed graphing. This includes minute to minute numbers on maptick td and pop, alongside some more complex graphs that to be frank with you I've yet to sort. They're stored in raw values, but presented in change over time to make reading them easier. That's what this step exists for, turning them into delta values.

You can specify what path to use yourself, the system will fuzzy match for it, or you can just call the script with no input and insert what round id you want to graph.

### [single_round](single_round/single_round.gnuplot)

Graphs the data created by SingleRound. As I mentioned before it splits things up into 6 png files, the first contains most traditionally useful information, the rest are just dumps of maptick statistics. Need a better way of handling these

Calling the gnuplot manually will let you name things a bit more uniquely, if you'd like. If you don't it'll be organized by unix timestamp inside [single_round](single_round/)