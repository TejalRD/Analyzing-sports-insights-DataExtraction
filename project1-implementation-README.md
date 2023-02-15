Analyzing Sports insights on Twitter, Reddit and Youtube 


## Project Abstract

Sites like Twitter, Reddit and Youtube have given people a platform to engage with a single piece of content in many different ways. For developers, this presents an opportunity to measure different metrics on different platforms, and derive insights from the vast amount of data being generated. 
We have two major sporting events comingup: FIFA World cup Qatar 2022 and ICC Men’s T20 Worldcup. In this project, we use three major social media platforms: Twitter, Reddit and Youtube to analyze the popularity of these events indifferent parts of the world, the athletes and how the public engages with them and lastly, abusive content generated through thecourse of the events.

## Tech-stack

* `python` - The project is developed and tested using python v3.8. [Python Website](https://www.python.org/)
* `request` - Request is a popular HTTP networking module(aka library) for python programming language. [Request Website](https://docs.python-requests.org/en/latest/#)
* `MongoDB`- This project uses NoSQL for saving collected data. [MongoDB Website] (https://www.mongodb.com/docs/manual/) 
* `pymongo` - This is a python distribution to work with MongoDB from Python
* `googleapiclient` - This project uses the google API python library to work with the YouTube API.


## Three data-source documentation

This section must include two things for each source: (1) A specific end-point URL(aka API) or Website link if you are crawling web-pages (2) Documentation of the API

* `Twitter`
  * [Twitter Stream API V2](https://developer.twitter.com/en/docs/tutorials/consuming-streaming-data) - <A stream API from Twitter which opens a single connection between the python application and the API, with new results being sent through that connection whenever new matches occur.>

* `Reddit` - We are using `r/soccer`, `r/soccercirclejerk`,`r/worldcup`,`r/cricket`,`r/cricketshitpost`
  * [r/soccer](https://reddit.com/r/soccer) - <Posts related to soccer to track the FIFA World Cup data>
  * [r/cricket](https://reddit.com/r/cricket) - <Posts related to crciket to track the T20 Cricket world cup data>
  * [API-Link](https://www.reddit.com/dev/api/) - <The API provides tools or functions to access the reddit data>

* `YouTube` - <The API provides functions to search for videos matching specific search terms, topics, locations, publication dates, etc. The APIs search.list method also supports searches for playlists and channels.>
  * [API-Link](https://developers.google.com/youtube/v3) 

## System Architecture

![System Architecture](https://drive.google.com/file/d/10-ayFgZ9du7IOmFlDJyGu4ZsuiZtV2R8/view?usp=sharing)


## How to run the project?

Install `Python` and `MongoDB`

```bash
pip install pymongo
pip install google-api-python-client
pip install schedule
pip install requests
pip install argparse
pip install httplib2


python3 youtubeCricket.py
python3 youtubeFootball.py
python3 redditscraper_final.py
python3 FIFA_twitter.py
python3 T20_twitter.py

```
**NOTE: You must mention all required details to run your project. We will not fix any `compilation` or `runtime` error by ourself. If something needs to be installed, mention it!**

## Database schema - NoSQL 

**The Data is stored inside MongoDB database. There are 6 collections in the database, 3 for storing cricket data from twitter, reddit and Youtube and 3 for football data from the same platforms.

Commands to run inside Mongo shell:
mongo
show dbs
use p1
show collections
db.collection_name.find()

```bash

collection_1: twitter_crciket
{
  "id": tweet id,
  "text": tweet text;
}

collection_2: twitter_football
{
  "id": tweet id,
  "text": tweet text;
}

collection_3: reddit_cricket
{
  "id": author id,
  "text"comment text: 
  
}

collection_4: reddit_football
{
 "id": author id,
  "text"comment text: 
  
}

collection_5: youtube_cricket
{
  "id": author,
  "text": comment text;
}

collection_6: youtube_football
{
  "id": author,
  "text": comment text;
}
```




