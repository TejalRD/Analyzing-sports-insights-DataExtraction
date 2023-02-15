import time
import schedule
import argparse
from pprint import pprint
from httplib2 import Authentication
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pymongo import MongoClient

try:
    connect = MongoClient()
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

# connecting or switching to the database p1
db = connect.p1


def get_youtube():
  DEVELOPER_KEY = 'AIzaSyDyXuWp36Xb3FtIXC7c6u9rUdrHpy9pr8Q'
  YOUTUBE_API_SERVICE_NAME = 'youtube'
  YOUTUBE_API_VERSION = 'v3'
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
  developerKey=DEVELOPER_KEY)

  return youtube

def youtube_search(options):
  
  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = get_youtube().search().list(
    q=options.q,
    part='id,snippet',
    maxResults=options.max_results
  ).execute()

  #pprint(search_response)
  videos = []
  channels = []
  playlists = []
  vid = []
  channel_ids = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get('items', []):
    if search_result['id']['kind'] == 'youtube#video':
      videos.append('%s (%s)' % (search_result['snippet']['title'],
                                 search_result['id']['videoId']))
      vid.append(search_result['id']['videoId'])
      if search_result['snippet']['channelId'] not in channel_ids:
        channel_ids.append(search_result['snippet']['channelId'])

    elif search_result['id']['kind'] == 'youtube#channel':
      channels.append('%s (%s)' % (search_result['snippet']['title'],
                                   search_result['snippet']['channelId']))
      if search_result['snippet']['channelId'] not in channel_ids:
        channel_ids.append(search_result['snippet']['channelId'])
    elif search_result['id']['kind'] == 'youtube#playlist':
      playlists.append('%s (%s)' % (search_result['snippet']['title'],
                                    search_result['id']['playlistId']))
      if search_result['snippet']['channelId'] not in channel_ids:
        channel_ids.append(search_result['snippet']['channelId'])
  

  print('Videos:\n', '\n'.join(videos), '\n')
  print('Channels:\n', '\n'.join(channels), '\n')
  print('Playlists:\n', '\n'.join(playlists), '\n')
  print('ID:\n', '\n'.join(vid), '\n')
  print('Channel ID:\n', '\n'.join(channel_ids), '\n')
  extractComments(vid)
  
  '''if 'FIFA' in search_response:
    collection=db.youtube_cricket
    extractComments(vid,db.youtube_cricket)
  elif 'T20' in search_response:
    collection=db.youtube_football
    extractComments(vid,db.youtube_football)'''



def extractComments(vid):

  youtube = get_youtube()
  for id in vid:
    request = youtube.commentThreads().list(
      part = "snippet",
      videoId = id
    )
  response = request.execute()

  for item in response['items']:
    comments = item['snippet']['topLevelComment']
    author = comments['snippet']['authorDisplayName']
    comment_text = comments['snippet']['textDisplay']
    
    #creating a dict to store author and comment
    comment_dict={author:comment_text}
    
    #insert each tuple in the MongoDB collection
    collection.insert_one({author:comment_text})  
    
    print(comment_dict)
     

def extractFootball():

  parser = argparse.ArgumentParser()
  parser.add_argument('--q', help='Search term', default='FIFA world cup 2022')
  parser.add_argument('--max-results', help='Max results', default=50)
  args = parser.parse_args()
  try:
    youtube_search(args)
  except(HttpError):
    print('An HTTP error')


if __name__ == '__main__':

  #set the collection name
  collection = db.youtube_football
  extractFootball()
  #scheduler will keep executing this code after every 30 seconds
  schedule.every(60).seconds.do(extractFootball)
  while True:
  #Suspend the execution for 30 secs if there are pending tasks
    schedule.run_pending()
    time.sleep(60) #delay of 60 minutes

  
