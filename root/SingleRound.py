import csv
import glob
import sys
import subprocess
import os.path

#output_loc = "maptick/"
#if not os.path.exists(output_loc):
#    os.makedir(output_loc)
    
output_to = "single_round/temporary"
read_from = "output/"
sendmaps_starting = ["send_maps", "initial_house", "cleanup", "client_loop", "per_client", "deleted_images", "hud_update", "statpanel_update", "map_data", "check_eye_pos", "update_chunks", "turfmap_updates", "changed_turfs", "turf_chunk_info", "obj_changes", "mob_changes", "send_turf_vis_conts", "pending_animations", "look_for_movable_changes", "check_turf_vis_conts", "check_hud/image_vis_contents", "turfs_in_range", "movables_examined"]
sendmaps_grunge = []
for name in sendmaps_starting:
    sendmaps_grunge += [name + "_count"]

fieldnames = ["time", "players", "maptick", "tidi_avg"]

path = ""
if len(sys.argv) > 1:
    path = f"{sys.argv[1]}*"
else:
    id = int(input("What round number do you want to graph?\n"))    
    path = f"{read_from}*{id}*.csv"

print(f"Searching for: ({path})")
inputfiles = glob.glob(path)
print(inputfiles)

f_name = inputfiles[0]

trueval = {}

csvfile = open(f_name, newline='')
reader = csv.DictReader(csvfile)

output = open(f"{output_to}.csv", 'w')
writer = csv.DictWriter(output, fieldnames=fieldnames+sendmaps_grunge+sendmaps_starting)
writer.writeheader()

for row in reader:
    data = {}

    lasttime = 0 
    if "time" in trueval:
        lasttime = trueval["time"]
    time = float(row["time"])
    trueval["time"] = time

    deltatime = time - lasttime
    for name in (fieldnames + sendmaps_grunge):
        if name not in row:
            data[name] = 0
            continue
        data[name] = float(row[name])           
    for name in sendmaps_starting: 
        if name not in row:
            data[name] = 0
            continue
        lastname = 0
        if name in trueval:
            lastname = trueval[name]   

        nameval = float(row[name])        
        trueval[name] = nameval

        deltaname = nameval - lastname #We're guarenteed that this number will just keep going up, so this is safe
        namepersec = deltaname / deltatime #We want to save the ____ per second in a period, to look for spikes
        data[name] = namepersec

    writer.writerow(data)
    
csvfile.close()
output.close()

properties = f_name.split("-") #This will get messy if you have a - in the system path

if len(f_name.split("-")) < 2:
    print(f"ERROR: [{f_name}] Is being improperly parsed")
id = f_name.split("-")[1] #The second item in this list should be id
map = f_name.split("-")[2].split(".")[0] #The third item is the map name + the .csv bit. Let's cut that out.
print(f"Done with [{id}] [{map}]")
