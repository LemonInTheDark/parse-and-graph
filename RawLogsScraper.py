from bs4 import BeautifulSoup
import json
import requests
import os.path

#Example inputs for the headers to pack with the request. Put yours in a dictonary in cookie_file
fakingIdentity = {
    "Host": "tgstation13.org",
    "User-Agent": "PISSOFF",
    "Accept": "Remember to not accept zip files",
    "Accept-Language": "hhhhhhhhhhh",
    "Referer": "Pick Your Poison",
    "Connection": "keep-alive",
    "Cookie": "Do not post this publically anywhere 4head",
    "Upgrade-Insecure-Requests": "1"
}

serverNames = ["manuel", "basil", "sybil", "terry"]

outputFolder = "output/"
cookie_file = "mood.json"

def get_raw_logs(requestTarget) :
    response = requests.get(requestTarget, headers = fakingIdentity)
    if response.status_code != 200: #If we time out don't spawm mso too hard
        print(f"A raw request failed to return 200 OK, instead returning [{str(response.status_code)}]. stopping investigation")
        return
    return response

def scrape(url):
    print(f"Scraping [{url}] ...")

    #Ready for some hellcode to prevent scraping 2010 logs?
    split_url = url.split("/")
    split_url.reverse() #Flip it so we can read top down
    #Fully functional performance logging was merged on the 10th of November 2020, this prevents overshooting when taking the initial copy of the logs 
    if split_url[1] == "11" and split_url[2] == "11" and split_url[3] == "2020":  
        return -1

    files_to_investigate = listFD(url)
    files_to_investigate.reverse() #Reverse so you don't fail when trying to read a folder that existed before the logs existed

    if not files_to_investigate: #If you time out, end execution
        print(f"No files in {str(files_to_investigate)}")
    for file in files_to_investigate:
        if file == "../":
            continue
        if "." not in file:
            if scrape(url + file) == -1: #Propogate failure up the chain
                return -1 
        if ".csv" not in file : #Not what we're after
            continue
        return readFile(url + file, file) #Propogate failure up the chain
        
def listFD(url):
    page = get_raw_logs(url)
    if not page:
        print(f"The page does not exist [{str(page)}]") 
        return
    soup = BeautifulSoup(page.text, 'html.parser')
    return [node.get('href') for node in soup.find_all('a')]

def readFile(file, path):
    response = get_raw_logs(file)
    #The exists check prevents overscanning, if you fuck something up comment it out 
    if not response or os.path.exists(outputFolder + path): 
        return -1
    print(f"Writing out [{file}]")
    file = open(outputFolder + path, 'w') 
    file.write(response.text)
    file.close()

do_not_post_this_4head = open(cookie_file)
fakingIdentity = json.load(do_not_post_this_4head) #Loads a .json file containing the cookie and other params to send to mso
do_not_post_this_4head.close()

if not os.path.exists(outputFolder):
    os.mkdir(outputFolder)

for name in serverNames:
    url = f"https://tgstation13.org/raw-logs/{name}/data/logs/"
    scrape(url)
