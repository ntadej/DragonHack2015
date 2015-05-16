from bs4 import BeautifulSoup
import requests

possibleBPM = ["80-100", "100-120", "120-140", "140-150","150-160","160-170","170-190"]
possibleGenre = ["Alternative", "Alternative%2FElect.", "Country", "Dance", "Dubstep", "Hip-Hop%2FRap", "Latin", "Pop", "Reggae", "Rock", "R%26B%2FSoul", "Contemporary+Jazz", "Mainstream+Jazz"]

url = "http://jogtunes.com/jtc/jtctuneschoicesigned.php?"

def getBPMRange(bpm):
    #returns String (which is part of get request) of BPM range we're searching for
    if bpm < 100:
        return possibleBPM[0]
    if bpm < 120:
        return possibleBPM[1]
    if bpm < 140:
        return possibleBPM[2]
    if bpm < 150:
        return possibleBPM[3]
    if bpm < 160:
        return possibleBPM[4]
    if bpm < 170:
        return possibleBPM[5]
    if bpm >= 170 and bpm < 220:
        return possibleBPM[6]
    return "BPM"

def getListHTML(bpm="BPM", genre="Genre", artist=""):
    #Returns html that contains all the <tr> elements on the page
    newUrl=url + 'x='+bpm+'&q='+genre+'&a='+artist+'&Submit=Submit'
    r  = requests.get(newUrl)
    html = r.text
    return html

def getSongsInArray(htmlList):
    #acceps html from getListHTML() and returns array with Strings of names of songs
    soup = BeautifulSoup(getListHTML())
    allrows = soup.findAll('font', color="#000000")
    songs = []
    counter = 0
    for row in allrows:
        if counter % 7 == 0:
            songs.append(row.text)
        counter+=1
    return songs

def getArtistsInArray(htmlList):
    #accepts html from getListHTML() and returns array with Strings of names of artists
    soup = BeautifulSoup(getListHTML())
    allrows = soup.findAll('font', color="#000000")
    artists = []
    counter = 0
    for row in allrows:
        if counter % 7 == 1:
            artists.append(row.text)
        counter+=1
    return artists

html = getListHTML()
array = getArtistsInArray(html)

for song in array:
    print(song)

print(getBPMRange(150))
