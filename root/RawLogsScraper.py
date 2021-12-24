import glob
import traceback
import datetime
import json
import requests
import os.path

#Example inputs for the headers to pack with the request. Put yours in a dictonary in cookie_file
fakingIdentity = {
    "Host": "tgstation13.org",
    "User-Agent": "Default Graphing Scraper (Lemon Scented)",
    "Accept": "Remember to not accept zip files",
    "Accept-Language": "hhhhhhhhhhh",
    "Referer": "Pick Your Poison",
    "Connection": "keep-alive",
    "Cookie": "Do not post this publically anywhere 4head",
    "Upgrade-Insecure-Requests": "1"
}

## CONSTANTS

# The last workable round 
ON_THE_MORNING_OF_THE_FIRST_DAY = 150043

## CONFIG

# Main servers, let's not pull ehalls since that just muddles data, and campbell because the logs aren't in the same setup yet
serverNames = ["manuel", "basil", "sybil", "terry"]

# Folder to write our rounds into
outputFolder = "output/"

# Metadata folder
dataFolder = "data/"

# Log folder
logFolder = f"{dataFolder}logs/"

# File to write the info about our currently scraped rounds into
# Holds info in the form [server, target round, last stored round]
dataFile = f"{dataFolder}scraping.json"

# How many files to hold in the buffer before writing
bufferSize = 20

## VARIABLES

# Our current meta scraped info. Saves a file read
scraped_info = []

# Our current "target" round. Typically ON_THE_MORNING_OF_THE_FIRST_DAY
target_round = ON_THE_MORNING_OF_THE_FIRST_DAY

# How many times to retry a query before giving up and failing

retry_limit = 3

# SETUP

if not os.path.exists(outputFolder):
    os.mkdir(outputFolder)

if not os.path.exists(dataFolder):
    os.mkdir(dataFolder)

if not os.path.exists(logFolder):
    os.mkdir(logFolder)

if not os.path.exists(dataFile):
    file = open(dataFile, 'w')
    file.close()

readFile = open(dataFile, 'r') 
deets = readFile.read()
if len(deets):
    scraped_info = json.loads(deets)
readFile.close()


class ScrapingError(Exception):
    pass

class CommunicationBreakdownError(ScrapingError):
    """Exception raised when networking calls fail.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class Buffer:

    def __init__(self, size, server, lastUrl = ""):
        self.size = size
        # List of [url, fileName, text]s
        self.fileBuffer = []
        # The server we're currently iterating
        self.server = server
        # Our last saved url
        self.previousUrl = lastUrl

    def dumpBuffer(self):
        if len(self.fileBuffer) == 0:
            return
        lastUrl = ""
        for info in self.fileBuffer:
            lastUrl = info[0]
            filename = info[1]
            text = info[2]
            file = open(filename, 'w') 
            file.write(text)
            file.close()

        writeDataFile(self.server, lastUrl, self.previousUrl)
        self.previousUrl = lastUrl
        
        self.fileBuffer = []
        print("Flushed Buffer")

    def writeToBuffer(self, url, fileName, text):
        self.fileBuffer += [[url, fileName, text]]
        if len(self.fileBuffer) < self.size:
            return
        self.dumpBuffer()

def writeDataFile(server, roundUrl, previousUrl):
    master_info = scraped_info
    
    handled = False
    for info in master_info:
        if info[0] != server:
            continue
        if info[1] != previousUrl:
            continue
        # Update our "last round"
        info[1] = roundUrl
        handled = True
        break

    if not handled:
        master_info += [[server, roundUrl]]
    
    print(master_info)
    file = open(dataFile, 'w')
    # Store it, so failures don't fuck us over
    json.dump(master_info, file)
    file.close()

def clearDataFile():
    why_python = scraped_info
    why_python.clear()
    file = open(dataFile, 'w')
    # Goodbye honey
    file.write("")
    file.close()    


#Only uncomment these if you for some reason need to read raw logs

#owning mso with facts and logic (you need beautiful soup to parse raw logs for reasons)
#from bs4 import BeautifulSoup
#cookie_file = "mood.json"
#do_not_post_this_4head = open(cookie_file) 
#fakingIdentity = json.load(do_not_post_this_4head) #Loads a .json file containing the cookie and other params to send to mso
#do_not_post_this_4head.close()

def get_url(requestTarget) :
    for i in range(1, retry_limit):
        response = requests.get(requestTarget, headers = fakingIdentity)
        if response.status_code != 200: #If we time out don't spawm mso too hard
            print(f"A raw request failed to return 200 OK, instead returning [{str(response.status_code)}]")
            continue
        return response
    print("Failed too many times, stopping execution")
    raise CommunicationBreakdownError

def scrape(url, serverName, fileBuffer, newestAllowed = 0):
    if not fileBuffer:
        fileBuffer = Buffer(bufferSize)

    if newestAllowed and urlAge(url) >= newestAllowed:
        print(f"{url} was too recent, skipping")
        return

    print(f"Scraping [{url}] ...")

    files_to_investigate = listFD(url)
    files_to_investigate.reverse() #Reverse so you don't fail when trying to read a folder that existed before the logs existed

    if not files_to_investigate: #If you time out, step up a level
        print(f"No files in {str(files_to_investigate)}")
    for entry in files_to_investigate:
        filename = entry["name"]
        newUrl = f"{url}/{filename}"
        if entry["type"] == "directory":
            errorCode = scrape(newUrl, serverName, fileBuffer, newestAllowed)
            if errorCode: #Propogate failure up the chain
                return errorCode
            continue
        #performance files are formatted like this
        #perf-roundid-map-server.csv.gz
        if filename.split("-")[0] != "perf" : #Not what we're after
            continue
        return readFile(newUrl, filename, serverName, fileBuffer) #Propogate failure up the chain
        
    # Ready for some hellcode to prevent scraping 2010 logs?
    round_name = url.split("/")[-1] 

    # Format is year/month/day/round, if we're not a round, keep going
    if "round" in round_name:
        # Fully functional performance logging was merged on the 10th of November 2020, this prevents overshooting when taking the initial copy of the logs 
        current_id = round_name.split("-")[1] 
        if current_id.isnumeric() and int(current_id) <= target_round:  
            return -1

#Returns a list of dicts in the form {name, type (directory, file), mtime, size (for files)}
def listFD(url):
    jsonUrl = f"{url}/?index_format=json"
    jsonPage = get_url(jsonUrl)
    if not jsonPage:
        print(f"The page does not exist [{jsonUrl}]") 
        return
    return json.loads(jsonPage.text)

#Uncomment and implement if you want to parse raw files
#def listFDSoupy(url):
    #page = get_url(url)
    #if not page:
    #    print(f"The page does not exist [{str(page)}]") 
    #    return
    #soup = BeautifulSoup(page.text, 'html.parser')
    #return [node.get('href') for node in soup.find_all('a')]

def readFile(url, name, serverName, fileBuffer):
    response = get_url(url)
    name = name.rstrip('.gz')
    name_parts = name.split(".")
    name_parts[0] += f"-{serverName}"
    name = ".".join(name_parts)
    filename = outputFolder + name

    #The exists check prevents overscanning, if you fuck something up comment it out 
    if not response: 
        return -1
    
    if os.path.exists(filename):
        return -1
    
    fileBuffer.writeToBuffer(url, filename, response.text)

def roundAge(round):
    # If you're not a string (Not a round id) I'm not interested
    if round.isnumeric():
        return int(round)
    
    id = round.split("-")[1]
    # If the server loses connection to the db for a period it will resort to ordering rounds by I think HH.MM.SS UTC
    # We can't use this, so just drop it  
    if not id.isnumeric():
        print(f"[round] was not capable of being sanely converted into a number")
        return 0
    # Lets make our id part of the number, but a fraction. Hopefully this makes things cleaner
    return float("0." + id)

# Gets the "Age" of a url, good for ordering them
def urlAge(url):
    # Day month year, we assume only 3 valid didgets in the url
    dateInfo = [1970, 1, 1]
    didgetsFound = 0
    portions = url.split("/")
    for portion in portions:
        if not portion.isnumeric():
            continue
        value = int(portion)
        dateInfo[didgetsFound] = value
        didgetsFound += 1
    
    time_since_epoch = datetime.datetime(dateInfo[0],dateInfo[1],dateInfo[2]) - datetime.datetime(1970,1,1)
    age = time_since_epoch.total_seconds()

    # No actual age? end it lads
    if not age:
        return age
    
    # https://tgstation13.org/parsed-logs/manuel/data/logs/2021/12/09/round-174460
    # 1 2 3 4 5 6 7 8 9 10 /s, so we take the 10th section, if it exists
    if len(portions) < 11:
        return age

    return age + roundAge(portions[10])

# Finds pockets of unpulled rounds
def findPockets():
    allFilenames = glob.glob(f"{outputFolder}*.csv")
    
    # Pull out just the round ids from the file names
    roundIds = []
    for filename in allFilenames:
        round = filename.split("/")[-1]
        # prefs-id-map-server.csv
        id = round.split("-")[1]
        if not id.isnumeric():
            print(f"({filename})'s {id} was not a number?")
            continue
        roundIds += [int(id)]
    roundIds.sort()

    # Now, we look for ranges with holes
    # List of "starts" of holes
    missing_ids = []
    lastId = 0
    for id in roundIds:
        if not lastId:
            lastId = id - 1
        # Are we properly in order
        if id - lastId > 1:
            missing_ids += [lastId + 1]
        lastId = id
    
    print(missing_ids)

# Cleans pockets of unpulled deets from the data
def healPockets():
    # If you've got pockets to heal, nuke the compiled rounds data file
    # Since you'll want a full rebuild
    if len(scraped_info):
        file = open(f"{dataFolder}last_run.dat", 'w')
        file.write("")
        file.close()

    # Anyway, time to heal our pockets
    for unfinishedInfo in scraped_info:
        server = unfinishedInfo[0]
        lastUrl = unfinishedInfo[1]
        
        # Gets our url's age
        age = urlAge(lastUrl)

        url = f"https://tgstation13.org/parsed-logs/{server}/data/logs"
        buffer = Buffer(bufferSize, server, lastUrl)
        

        print(f"{lastUrl}'s age is {age}")
        # Scrape based on our age, ignore any existing file hits
        scrape(url, server, buffer, age)
        buffer.dumpBuffer()

    clearDataFile()

def pullNew():
    for name in serverNames:
        url = f"https://tgstation13.org/parsed-logs/{name}/data/logs"
        buffer = Buffer(bufferSize, name)
        
        scrape(url, name, buffer)
        buffer.dumpBuffer()
        # Finished with this server, clear the data
        clearDataFile()

# Normal operation
def standard():
    healPockets()
    pullNew()

try:
    standard()
except:
    time = datetime.datetime.now().timestamp()
    file = open(f"{logFolder}{time}.log", "w")
    file.write(traceback.format_exc())
    file.close()