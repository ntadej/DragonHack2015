#!/usr/bin/python
## Needs pip install --upgrade google-api-python-client

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
from bs4 import BeautifulSoup
import requests
import json
import random

class Search:
  # Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
  # tab of
  #   https://cloud.google.com/console
  # Please ensure that you have enabled the YouTube Data API for your project.
  DEVELOPER_KEY = "AIzaSyBquAlaRWuIWh2sDGbsJ-aSLxE229hhKSo"
  YOUTUBE_API_SERVICE_NAME = "youtube"
  YOUTUBE_API_VERSION = "v3"
  possibleBPM = ["80+and+100", "100+and+120", "120+and+140", "140+and+150","150+and+160","160+and+170","170+and+190"]
  possibleGenre = ["Alternative", "Alternative%2FElect.", "Country", "Dance", "Dubstep", "Hip-Hop%2FRap", "Latin", "Pop", "Reggae", "Rock", "R%26B%2FSoul", "Contemporary+Jazz", "Mainstream+Jazz"]

  url = "http://jogtunes.com/jtc/jtctuneschoicesigned.php?"


  def __init__(self):
    argparser.add_argument("--q", help="Search term", default='Rickroll')
    argparser.add_argument("--max-results", help="Max results", default=2)
    self.used = []

  def clear(self):
    self.used = []

  def getItunesLink(self, song):
    #takes concaturated string of artist and song name as arg
    iTunesUrl = "https://itunes.apple.com/search?term="
    iTunesTerm = song
    iTunesLimit = "&limit=1"
    r  = requests.get(iTunesUrl+iTunesTerm+iTunesLimit)

    json_result = json.loads(r.text).get('results')

    try:
      for key, value in json_result[0].items():
        if key == "trackViewUrl":
          return value
    except IndexError:
      return 'http://www2.rdrop.com/~paulmck/DemoGods/'

  def search_all(self, bpm, debug=False):
    html = self.getListHTML(self.getBPMRange(bpm))
    songs = self.getSongsInArray(html)
    artists = self.getArtistsInArray(html)
    oboje = []
    for i in range(len(songs)):
      oboje += [artists[i] + ' - ' +songs[i]]
    random.shuffle(oboje)
    for s in oboje:
      if s in self.used:
        continue
      else:
        self.used += [s]
        song = s
        break
    else:
      song = 'Not found'
    if debug:
      print('Song found', s)
    #return s
    print(self.getItunesLink(song))
    yid = self.search_by_word(song)
    return yid


  def getBPMRange(self, bpm):
    #returns String (which is part of get request) of BPM range we're searching for
    if bpm < 100:
        return self.possibleBPM[0]
    if bpm < 120:
        return self.possibleBPM[1]
    if bpm < 140:
        return self.possibleBPM[2]
    if bpm < 150:
        return self.possibleBPM[3]
    if bpm < 160:
        return self.possibleBPM[4]
    if bpm < 170:
        return self.possibleBPM[5]
    if bpm >= 170 and bpm < 220:
        return self.possibleBPM[6]
    return "BPM"


  def getListHTML(self, bpm="BPM", genre="Genre", artist=""):
    #Returns html that contains all the <tr> elements on the page
    newUrl = self.url + 'x=' + bpm + '&q=' + genre + \
             '&a=' + artist + '&Submit=Submit'
    r  = requests.get(newUrl)
    html = r.text
    return html

  def getSongsInArray(self, htmlList):
    #acceps html from getListHTML() and returns array with Strings of names of songs
    soup = BeautifulSoup(htmlList)
    allrows = soup.findAll('font', color="#000000")
    songs = []
    counter = 0
    for row in allrows:
        if counter % 7 == 0:
            songs.append(row.text)
        counter+=1
    return songs

  def getArtistsInArray(self, htmlList):
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

  def youtube_search(self, options):
    print('here')
    youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
      developerKey=self.DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    # print('here')
    search_response = youtube.search().list(
      q=options.q,
      part="id,snippet",
      maxResults=options.max_results
    ).execute()

    videos = []
    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
      if search_result["id"]["kind"] == "youtube#video":
        videos.append(search_result["id"]["videoId"])
    #print("Videos:\n", "\n".join(videos), "\n")
    return videos[0]

  def search_by_word(self, search_term):
    args = argparser.parse_args()
    args.q = search_term

    try:
      return self.youtube_search(args)
    except HttpError as e:
      print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
      return ''



if __name__ == '__main__':
  A = Search()
  print(A.search_by_word('goska'))
  print(A.search_all(80, debug = True))
  print(A.search_all(80, debug = True))
  print(A.search_all(80, debug = True))
