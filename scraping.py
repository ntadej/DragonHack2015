from bs4 import BeautifulSoup
import requests






def getArtistsInArray(htmlList):
    #accepts html from getListHTML() and returns array with Strings of names of artists
    soup = BeautifulSoup(htmlList)
    allrows = soup.findAll('font', color="#000000")
    artists = []
    counter = 0
    for row in allrows:
        if counter % 7 == 1:
            artists.append(row.text)
        counter+=1
    return artists

html = getListHTML(getBPMRange(80))
artists = getArtistsInArray(html)
songs = getSongsInArray(html)

for artist, song in zip(artists, songs):
    print(artist, song)
