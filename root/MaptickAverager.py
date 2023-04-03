import csv
import glob
import os
import os.path
import sys
import enum
from enum import auto

MAX = sys.float_info.max

output_loc = "compiled/"
if not os.path.exists(output_loc):
    os.makedir(output_loc)

output_to = f"{output_loc}maptick.csv"

data_file = "data/last_run.dat"
old_data_file = f"{output_loc}last_run.dat"

# converts a float input measured in seconds to one in microseconds


def to_microseconds(value):
    return value * 1000 * 1000

# Converts a log file into a dict


def log_file_to_dict():
    write_to = {}
    file_path = data_file

    if not os.path.exists(file_path):
        file_path = old_data_file
        if not os.path.exists(file_path):
            return write_to

    # A data file holding info about the last "compile"
    # In the format Key:Data\n
    info_file = open(file_path, 'r')
    info = info_file.read()
    info_file.close()

    info = info.split("\n")  # Split the file into lines
    for line in info:
        packet = line.split(":")  # Convert the file into a dict
        if not line:  # Damn new lines
            continue
        write_to[packet[0]] = str(packet[1])

    return write_to

# Converts a log file into a dict, in the format described above


def dict_to_log_file(dict):
    write_string = ""
    file_path = data_file

    for key in dict:
        write_string += f"{key}:{dict[key]}\n"

    write_string.strip("\n")

    info_file = open(file_path, 'w')
    info_file.write(write_string)
    info_file.close()

# Returns true if the two dicts match in terms of method, false otherwise


def compare_dict_methods(dict1, dict2, compare_by):
    for entry in compare_by:
        if entry not in dict1 and entry not in dict2:
            print(f"{entry} was in nothing, wtf")
            continue
        # One file is newer then the other, do a full rerun
        if entry not in dict1 or entry not in dict2:
            print(f"The dat file was outdated")
            return False
        if float(dict1[entry]) != float(dict2[entry]):
            print(f"{entry} [{dict1[entry]}] != [{dict2[entry]}]")
            return False
    return True


def copy_dict_into_dict(copy_from, copy_into, keys_to_ignore):
    for key in copy_from:
        if key in keys_to_ignore:
            continue
        copy_into[key] = copy_from[key]

def round_binary_search(arr, look_for):
    look_for = int(look_for)
    low = 0
    high = len(arr) - 1
    mid = 0

    while low <= high:

        mid = (high + low) // 2

        # This will get messy if you have a - in the system path
        properties = arr[mid].split("-")
        # Hopefully the  second line in this file is always the round's id
        working_rnd_id = int(properties[1])
        if working_rnd_id < look_for:
            low = mid + 1
        elif working_rnd_id > look_for:
            high = mid - 1
        else:
            return mid

    # If we reach here, then the element was not present
    return -1


def file_binary_search(arr, look_for):
    look_for = int(look_for)
    low = 0
    high = len(arr) - 1
    mid = 0

    while low <= high:

        mid = (high + low) // 2

        # This will get messy if you have a - in the system path
        properties = arr[mid].split(",")
        # First line's always the id, right? RIGHT?
        working_rnd_id = int(properties[0])
        if working_rnd_id < look_for:
            low = mid + 1
        elif working_rnd_id > look_for:
            high = mid - 1
        else:
            return mid

    if mid <= 0:
        return mid  # This is for the empty files, since you can't take away more then nothing can you

    roundid = int(arr[mid].split(",")[0])
    lastmid = mid
    # While we're greater then the target round id
    while roundid >= look_for:
        if mid - 1 <= -1:  # If this is the last item in the list give up
            break
        lastmid = mid  # Set lastmid to our current value
        mid -= 1  # Lower mid by one
        roundid = int(arr[mid].split(",")[0])  # Set roundid to the new value

    # This will keep looping until we either hit the end, or go below the last round id
    # Should prevent rounding issues with the binary search

    # If we reach here, then the element was not present
    return lastmid


def make_list_into_string(headers):
    output = ""
    for header in headers:
        output += f"{header},"
    output = output.strip(",")
    output += "\n"
    return output


def turn_dict_into_comma_seperated_string(dict_to_convert, headers):
    output = ""
    for key in headers:
        output += f"{dict_to_convert[key]},"
    output = output.strip(",")
    output += "\n"
    return output


def recalculate_value(list, default_value, value_creator):
    current_val = list[0]
    first = list[1][0]
    list[1].pop(0)  # Remove the first item in the list
    if first == current_val:
        holder = default_value
        for value in list[1]:
            holder = value_creator(value, holder)
        if holder == default_value:
            holder = 0
        list[0] = holder


def add_new_value(list, new_value, value_creator):
    list[0] = value_creator(new_value, list[0])
    list[1] += [new_value]


# A dict of information about this run, used to determin if a full run is needed next time
data_log = {}

tags_to_compare_with = ["backward_avg", "forward_avg", "backward_bound","forward_bound", "starting_at", "highpass_threshold"]
tags_to_leave_pure = tags_to_compare_with + ["last_round_fully_processed"]
# A dict of information about the last run we did
old_log = log_file_to_dict()

# Modify these tochange the size of the moving average
movingbackward = 30
movingforward = 30
total_moving_space = movingbackward + movingforward

data_log["backward_avg"] = str(movingbackward)
data_log["forward_avg"] = str(movingforward)

# Modify these to effect the size of moving minimums and maximums. so how large should our bucket of items to min/max be basically
boundbackward = 20
boundforward = 20
total_bound = boundbackward + boundforward

data_log["backward_bound"] = str(boundbackward)
data_log["forward_bound"] = str(boundforward)

# Knock on wood
data_log["last_round_fully_processed"] = 10000000000

# A reminder of the farthest back you can go
ON_THE_MORNING_OF_THE_FIRST_DAY = 150043
# This is useful for making graphs that scale a little bit better, fucking carpets man
PAST_CARPETS = 156000

# What round id to start reading at
head_rnd = ON_THE_MORNING_OF_THE_FIRST_DAY
data_log["starting_at"] = head_rnd

highpass = 2.5  # Cuts out the pain stuff while still allowing the carpet bump to remain clear
data_log["highpass_threshold"] = highpass

keys_to_average = ["maptick_to_player", "maptick", "players", "td", "td_to_player", "sendmaps_cost_per_tick", "per_client", "look_for_movable_changes", "check_turf_vis_conts", "check_hud/image_vis_contents", "turfs_in_range", "obj_changes", "mob_changes", "movables_examined"]

input = glob.glob("output/*.csv")

# The index to start reading at
id_start_at = round_binary_search(input, head_rnd)
preserve_old_files = compare_dict_methods(
    data_log, old_log, tags_to_compare_with)

if preserve_old_files:
    round_start_at = old_log["last_round_fully_processed"]
    id_start_at = round_binary_search(input, round_start_at)

copy_dict_into_dict(old_log, data_log, tags_to_leave_pure)

fieldnames = keys_to_average.copy()
for key in keys_to_average:
    fieldnames += [f"avg_{key}"]
    fieldnames += [f"min_{key}"]
    fieldnames += [f"max_{key}"]

fieldnames = ["id"] + fieldnames

# I despise janitors
maps_we_care_about = ["Delta%20Station", "Ice%20Box%20Station",
                      "Kilo%20Station", "MetaStation", "Tramstation"]

# Dictionary of file names to dictionaries of data to be written later.
data = {}

# first pass of data parsing: populate the data dictionary with info
# for all round ids we've not ingested before
for index in range(id_start_at, len(input)):
    f_name = input[index]
    lines_read = 0
    maptick_total = 0
    player_total = 0
    td_total = 0

    has_sendmaps_profiler_logs = False

    csvfile = open(f_name, newline='')
    reader = csv.DictReader(csvfile)

    #raw_rows = csvfile.readlines()
    #rows_with_fields = dict(zip(reader.fieldnames, raw_rows))

    get_value = lambda row, row_stat, null_val=0: float(row.get(row_stat) or null_val) if row != None else null_val

    last_row = None

    # read all the data
    for row in reader:
        lines_read += 1
        last_row = row.copy()

        maptick_total += get_value(row, "maptick")
        player_total += get_value(row, "players")
        td_total += get_value(row, "tidi_avg")

    # the last row read is the final value for these
    sendmaps_total_cost = get_value(last_row, "send_maps")
    # have to use .get(index) or 0 because not all logs have these indices
    sendmaps_total_calls = get_value(last_row, "send_maps_count")
    if sendmaps_total_cost != 0.0:
        has_sendmaps_profiler_logs = True
        print("has_sendmaps_profiler_logs = True")

    sendmaps_client_cost = get_value(last_row, "per_client")
    sendmaps_client_calls = get_value(last_row, "per_client_count")

    movable_changes_cost = get_value(last_row, "look_for_movable_changes")
    movable_changes_calls = get_value(last_row, "look_for_movable_changes_count")

    check_turf_vis_contents_cost = get_value(last_row, "check_turf_vis_conts")
    check_turf_vis_contents_calls = get_value(last_row, "check_turf_vis_conts_count")

    check_hud_image_vis_contents_cost = get_value(last_row, "check_hud/image_vis_contents")
    check_hud_image_vis_contents_calls = get_value(last_row, "check_hud/image_vis_contents_count")

    loop_turfs_in_range_cost = get_value(last_row, "turfs_in_range")
    loop_turfs_in_range_calls = get_value(last_row, "turfs_in_range_count")

    obj_changes_cost = get_value(last_row, "obj_changes")
    obj_changes_calls = get_value(last_row, "obj_changes_count")

    mob_changes_cost = get_value(last_row, "mob_changes")
    mob_changes_calls = get_value(last_row, "mob_changes_count")

    movables_examined = get_value(last_row, "movables_examined")

    csvfile.close()

    # In the template perf-[roundid]-[mapname]-[servername].csv
    file_without_ending = f_name.split(".")[0]
    # This will get messy if you have a - in the system path
    properties = file_without_ending.split("-")
    if len(properties) < 3:
        print(f"ERROR: [{f_name}] Is being improperly parsed")
    id = properties[1]  # The second item in this list should be id
    map = properties[2]  # The third item is the map name
    # Fourth term's the server this round came from, we'll need that soon
    server = properties[3]

    if not id.isnumeric():
        print("Found a non numeric round id, [id], skipping")
        continue

    # There was a short period where we were parsing byond's maptick values incorrectly.
    # This lead to irrecovorably broken logs. This check exists to handle them
    # Let's try not to add any more yeah?
    intid = int(id)
    if intid >= 164722 and intid <= 164824:
        continue

    def average_if_valid(numerator, denominator): return numerator / denominator if denominator > 0 else 0
    def average_if_exists(numerator, denominator): return average_if_valid(numerator, denominator) if has_sendmaps_profiler_logs == True else 0

    td_per_player = average_if_exists(td_total, player_total)
    if td_per_player > 1.2:
        td_per_player = 0.6

    to_write = {}

    to_write["id"] = id
    to_write["maptick_to_player"] = average_if_valid(maptick_total, player_total)
    to_write["maptick"] = average_if_valid(maptick_total, lines_read)
    to_write["players"] = average_if_valid(player_total, lines_read)
    to_write["td"] = average_if_exists(td_total, lines_read)
    
    to_write["td_to_player"] = td_per_player

    to_write["sendmaps_cost_per_tick"] = to_microseconds(average_if_exists(sendmaps_total_cost, sendmaps_total_calls))
    to_write["per_client"] = to_microseconds(average_if_exists(sendmaps_client_cost, sendmaps_client_calls))
    to_write["look_for_movable_changes"] = to_microseconds(average_if_exists(movable_changes_cost, movable_changes_calls))
    to_write["check_turf_vis_conts"] = to_microseconds(average_if_exists(check_turf_vis_contents_cost, check_turf_vis_contents_calls))
    to_write["check_hud/image_vis_contents"] = to_microseconds(average_if_exists(check_hud_image_vis_contents_cost, check_hud_image_vis_contents_calls))
    to_write["turfs_in_range"] = to_microseconds(average_if_exists(loop_turfs_in_range_cost, loop_turfs_in_range_calls))
    to_write["obj_changes"] = to_microseconds(average_if_exists(obj_changes_cost, obj_changes_calls))
    to_write["mob_changes"] = to_microseconds(average_if_exists(mob_changes_cost, mob_changes_calls))
    to_write["movables_examined"] = average_if_exists(movables_examined, sendmaps_client_calls)

    # finalize our data collection by map, server, and generic single stat files
    pending = [map, server, "maptick", "highpass_maptick"]
    for index in pending:
        if index not in data:  # If one doesn't already exist, make a new list to put our map data into
            data[index] = []
        if index == "highpass_maptick" and (to_write["maptick_to_player"] > highpass):
            continue
        
        #print(to_write.copy())
        data[index].append(to_write.copy())

    print(f"Read [{id}] [{map}] [{server}]")

# Now that we've done a first pass, we need to go back over things again
# These are all the file names that need operating on
for index in data:
    working_list = data[index]
    # Before you open it for writing, if we're working from a starting point, write all the untouched lines into the cache
    write_to_file = ""

    write_to_file += make_list_into_string(fieldnames)

    key = f"last_round_fully_processed_{index}"
    # Preps existing csv files for our new input, careful this gets messy fast
    if preserve_old_files and id_start_at and key in old_log:
        round_start_at = old_log[key]

        round_start_at = min(int(round_start_at), int(
            old_log["last_round_fully_processed"]))
        read_from = open(f"{output_loc}{index}.csv", 'r')

        file_contents = read_from.read()
        read_from.close()

        file_contents = file_contents.strip("\n")

        file_contents = file_contents.split("\n")
        # Get rid of the first line, which should just be the headers
        file_contents = file_contents[1:]

        last_sane_round = file_binary_search(file_contents, round_start_at)
        if last_sane_round > 0:
            # Cut out the entries we're going to touch
            file_contents = file_contents[:last_sane_round + 1]
            write_to_file += "\n".join(file_contents)

    # If there's one item, I want this to be 0
    length_of_rows = len(working_list) - 1

    # These two dicts are key -> list[interested value, [list of members]]
    local_min = {}
    local_max = {}
    for key_type in keys_to_average:
        local_min[key_type] = [MAX, []]
        local_max[key_type] = [0, []]

    for i in range(length_of_rows):
        row = working_list[i]

        look_behind = i - movingbackward
        look_ahead = i + movingforward
        do_not_remove = False
        do_not_add = False

        # Wrapping, this is why there's those flat lines at the edges of the graph
        if look_behind < 0:
            # delta will be the remainder of look_ahead
            delta_behind = abs(look_behind)
            look_behind = 0
            look_ahead = min(look_ahead + delta_behind, length_of_rows)

        if look_ahead > length_of_rows:
            # delta will be the remainder of look_behind
            delta_ahead = look_ahead - length_of_rows
            look_ahead = length_of_rows
            look_behind = max(look_behind - delta_ahead, 0)

        if i - boundforward < 0:
            do_not_add = True

        if not i >= total_bound:
            do_not_remove = True

        totals = {}

        for key_type in keys_to_average:
            totals[key_type] = 0

            min_list = local_min[key_type]
            max_list = local_max[key_type]

            if not do_not_remove:
                recalculate_value(min_list, MAX, min)
                recalculate_value(max_list, 0, max)

            if do_not_add:
                continue

            newest_val = data[index][i][key_type]
            add_new_value(min_list, newest_val, min)
            add_new_value(max_list, newest_val, max)

        for ii in range(look_behind, look_ahead):  # Look through them all
            look_at = data[index][ii]
            for key_type in keys_to_average:
                totals[key_type] += look_at[key_type]

        # Add 1 so reading one line doesn't read an average of 0
        total_read = (look_ahead - look_behind) + 1

        for key_type in keys_to_average:
            row[f"avg_{key_type}"] = totals[key_type] / total_read
            row[f"min_{key_type}"] = local_min[key_type][0]
            row[f"max_{key_type}"] = local_max[key_type][0]

        write_to_file += turn_dict_into_comma_seperated_string(row, fieldnames)

        rnd_id = row["id"]
        print(f"Write [{index}] [{i}] [{rnd_id}]")

    last_good_subset_round = working_list[-min(
        len(working_list), total_moving_space)]["id"]
    data_log[key] = last_good_subset_round
    if index in maps_we_care_about:
        data_log["last_round_fully_processed"] = min(
            int(last_good_subset_round), int(data_log["last_round_fully_processed"]))

    output = open(f"{output_loc}{index}.csv", 'w')
    output.write(write_to_file)
    output.close()

dict_to_log_file(data_log)
