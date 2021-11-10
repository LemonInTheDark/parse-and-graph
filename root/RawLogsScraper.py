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

# Main servers, let's not pull ehalls since that just muddles data, and campbell because the logs aren't in the same setup yet
serverNames = ["manuel", "basil", "sybil", "terry"]

outputFolder = "output/"

#Only uncomment these if you for some reason need to read raw logs

#owning mso with facts and logic (you need beautiful soup to parse raw logs for reasons)
#from bs4 import BeautifulSoup
#cookie_file = "mood.json"
#do_not_post_this_4head = open(cookie_file) 
#fakingIdentity = json.load(do_not_post_this_4head) #Loads a .json file containing the cookie and other params to send to mso
#do_not_post_this_4head.close()

def get_raw_logs(requestTarget) :
    response = requests.get(requestTarget, headers = fakingIdentity)
    if response.status_code != 200: #If we time out don't spawm mso too hard
        print(f"A raw request failed to return 200 OK, instead returning [{str(response.status_code)}]. stopping investigation")
        return
    return response

def scrape(url, serverName):
    print(f"Scraping [{url}] ...")

    #Ready for some hellcode to prevent scraping 2010 logs?
    split_url = url.split("/")
    split_url.reverse() #Flip it so we can read top down
    #Fully functional performance logging was merged on the 10th of November 2020, this prevents overshooting when taking the initial copy of the logs 
    if split_url[1] == "11" and split_url[2] == "11" and split_url[3] == "2020":  
        return -1

    files_to_investigate = listFD(url)
    files_to_investigate.reverse() #Reverse so you don't fail when trying to read a folder that existed before the logs existed

    if not files_to_investigate: #If you time out, step up a level
        print(f"No files in {str(files_to_investigate)}")
    for entry in files_to_investigate:
        filename = entry["name"]
        newUrl = f"{url}/{filename}"
        if entry["type"] == "directory":
            if scrape(newUrl, serverName) == -1: #Propogate failure up the chain
                return -1 
            continue
        #performance files are formatted like this
        #perf-roundid-map-server.csv.gz
        if filename.split("-")[0] != "perf" : #Not what we're after
            continue
        return readFile(newUrl, filename, serverName) #Propogate failure up the chain
        
#Returns a list of dicts in the form {name, type (directory, file), mtime, size (for files)}
def listFD(url):
    jsonUrl = f"{url}/?index_format=json"
    jsonPage = get_raw_logs(jsonUrl)
    if not jsonPage:
        print(f"The page does not exist [{jsonUrl}]") 
        return
    return json.loads(jsonPage.text)

#Uncomment and implement if you want to parse raw files
#def listFDSoupy(url):
    #page = get_raw_logs(url)
    #if not page:
    #    print(f"The page does not exist [{str(page)}]") 
    #    return
    #soup = BeautifulSoup(page.text, 'html.parser')
    #return [node.get('href') for node in soup.find_all('a')]

def readFile(url, name, serverName):
    response = get_raw_logs(url)
    name = name.rstrip('.gz')
    name_parts = name.split(".")
    name_parts[0] += f"-{serverName}"
    name = ".".join(name_parts)
    filename = outputFolder + name

    #The exists check prevents overscanning, if you fuck something up comment it out 
    if not response or os.path.exists(filename): 
        return -1
    
    print(f"Writing out [{filename}]")
    file = open(filename, 'w') 
    file.write(response.text)
    file.close()

if not os.path.exists(outputFolder):
    os.mkdir(outputFolder)

for name in serverNames:
    url = f"https://tgstation13.org/parsed-logs/{name}/data/logs"
    scrape(url, name)
