import requests
import os
import json
import pymongo
from pymongo import MongoClient

try:
    connect = MongoClient()
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

# connecting or switching to the database p1
db = connect.p1

# creating or switching to twitter
collection = db.twitter_cricket
bearer_token = "AAAAAAAAAAAAAAAAAAAAAJyhigEAAAAA2WMYCkjTGBP5jb%2BsX3nVuJvaFqY%3D2GrFeS5t7ASm1p5DtKqZFNY4GnPBuBQPGYYJl2mTBotdwiNMoT"


def bearer_oauth_stream(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def bearer_oauth_location(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r


def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth_stream
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(f"Get Rules: {json.dumps(response.json())}")
    return response.json()


def delete_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    loader = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth_stream,
        json=loader,
    )
    if response.status_code != 200:
        raise Exception(
            f"Cannot delete rules (HTTP {response.status_code}): {response.text}"
        )
    print(f"Delete All Rules: {json.dumps(response.json())}")


def set_rules():
    cricket_rules = [
        {"value": "T20WC2022 ", "tag": "T20WC2022"},
        {"value": "T20WorldCup2022 ", "tag": "T20WorldCup2022"},
        {"value": "T20worldcup22 ", "tag": "T20worldcup22"}        
    ]   
    loader = {"add": cricket_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth_stream,
        json=loader,
    )
    if response.status_code != 201:
        raise Exception(
            f"Cannot add rules (HTTP {response.status_code}): {response.text}"
        )
    print(f"Set Rules: {json.dumps(response.json())}")


def get_tweet_location(tweet_id):
    tweet_fields = "expansions=referenced_tweets.id,author_id&user.fields=location&"
    url = f"https://api.twitter.com/2/tweets/{tweet_id}/"
    response = requests.request(
        "GET", url, auth=bearer_oauth_location, params=tweet_fields
    )

    if response.status_code != 200:
        raise Exception(
            f"Request returned an error: {response.status_code} {response.text}"
        )

    try:
        location = response_json["includes"]["users"][0]["location"]
    except:
        try:
        # This means that the tweet is a retweet, so now we will get the original tweet
            original_tweet_id = response_json["includes"]["tweets"][0]["id"]
            location = get_tweet_location(original_tweet_id)
        except:
            location= None
    return location


def get_stream():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream?tweet.fields=public_metrics",
        auth=bearer_oauth_stream,
        stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)["data"]
            # print(json.dumps(json_response, indent=4, sort_keys=True))
            tweet_id = json_response["id"]
            tweet_text = json_response["text"]
            tweet_retweet_count = json_response["public_metrics"]["retweet_count"]
            tweet_like_count = json_response["public_metrics"]["like_count"]
            tweet_location = get_tweet_location(tweet_id)
            
            tweet_dict={tweet_id:[tweet_text,tweet_retweet_count,tweet_like_count,tweet_location]}
            collection.insert_one({tweet_id:tweet_text})
            
            print(tweet_dict)
            '''
            print(f"Tweet ID: {tweet_id}")
            print(f"Tweet Text: {tweet_text}")
            print(f"Tweet Re-tweet count: {tweet_retweet_count}")
            print(f"Tweet Like Count: {tweet_like_count}")
            
            print(f"Tweet Locationt: {tweet_location}")
            print("---------------------------------")'''
            


def main():
    rules = get_rules()
    delete_rules(rules)
    set_rules()
    get_stream()


if __name__ == '__main__':
    main()             
   