import csv
import glob
import os
import os.path

output_loc = "maptick/"
if not os.path.exists(output_loc):
    os.makedir(output_loc)
    
output_to = output_loc + "maptick.csv"
movingmax = 249 #Max size of the moving average, starts at 0

fieldnames = ["id", "maptick_to_player", "avg_maptick_to_player", "maptick", "players", "avg_players"]
input = glob.glob("output/*.csv")
writers = {} #Dictionary of file names to csv writers
files = {} #Above but for csv files
movingavgs = {} #Contains types matched to list of the last item to be added, and a list of all items to average 

files["maptick"] = open(output_to, 'w')
writers["maptick"] = csv.DictWriter(files["maptick"], fieldnames=fieldnames)
writers["maptick"].writeheader()

for f_name in input:
    lines_read = 0
    maptick_total = 0
    player_total = 0

    csvfile = open(f_name, newline='')
    reader = csv.DictReader(csvfile)
    for row in reader:
        lines_read += 1
        maptick_total += float(row["maptick"])
        player_total += float(row["players"])
    csvfile.close()

    properties = f_name.split("-") #This will get messy if you have a - in the system path

    id = f_name.split("-")[1] #The second item in this list should be id
    map = f_name.split("-")[2].split(".")[0] #The third item is the map name + the .csv bit. Let's cut that out.

    maptick_by_players = 0
    avg_maptick = 0
    avg_players = 0
    if player_total:
        maptick_by_players = maptick_total / player_total
    if lines_read:
        avg_maptick = maptick_total / lines_read
        avg_players = player_total / lines_read

    if map not in writers: #If one doesn't already exist, make a new writer to put our map data into
        files[map] = open(output_loc + map + ".csv", 'w')
        writers[map] = csv.DictWriter(files[map], fieldnames=fieldnames)
        writers[map].writeheader()

    pending = [map, "maptick"]
    for index in pending:
        if index not in movingavgs: #Construct a new moving average
            movingavgs[index] = {}
            movingavgs[index]["maptick_over"] = [0, []]
            movingavgs[index]["player_count"] = [0, []]

        to_avg = {}
        to_avg["maptick_over"] = maptick_by_players
        to_avg["player_count"] = avg_players
        avgs = {}
        for key, value in movingavgs[index].items():
            head = movingavgs[index][key][0] #Gets the head of the moving average
            values = movingavgs[index][key][1] #Get the list of numbers
            
            if head >= len(values): #No infinite length lists yeah?
                values.insert(head, to_avg[key])
            else:
                values[head] = to_avg[key]

            movingavgs[index][key][0] = (head + 1) % movingmax #Move the head of our moving average
            

            total = 0
            count = 0
            for value in values:
                total += value
                count += 1
            
            avgs[key] = total / count #The average of the last "amount" of items

        writer = writers[index]
        writer.writerow({'id': id, 'maptick_to_player': maptick_by_players, 'avg_maptick_to_player': avgs["maptick_over"], 'maptick': avg_maptick, "players": avg_players, "avg_players": avgs["player_count"]})
    print("Wrote [" + id + "] [" + map + "]")

for name, file in files.items():
    file.close()