import requests
from pymongo import MongoClient


try:
    client = MongoClient()
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

# connecting or switching to the database
db = client.p1

# creating or switching to demoCollection

reddit_cricket_collection = db.reddit_cricket
reddit_football_collection = db.reddit_football

auth = requests.auth.HTTPBasicAuth('rZmRewfww0-Fh9WJWV_W0g', 'DQ_JPxv6pfmVonP_e639CKqqPs14GQ')
data = {'grant_type': 'password',
        'username': 'CS515Tester',
        'password': 'admintest99'}
userAgent = 'MyBot/0.0.1'
headers = {'User-Agent': 'MyBot/0.0.1'}

res = requests.post('https://www.reddit.com/api/v1/access_token',auth=auth, data=data, headers=headers)
TOKEN = res.json()['access_token']
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}
requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

soccer_done_flag = False
all_subreddits_done = False
f = open("input_football.txt", "r")
post_count =0

def sanitize_input(url):
            last_char = url[-1]
            if last_char == '/':
                url = url[:-1]
            url = f'{url}.json'
            return url

def authorize_me(line):
        line = line.strip()
        input_url = "https://oauth.reddit.com/r/{}/hot/".format(line)
        res = requests.get(input_url, headers=headers)
        return res


def get_replies(comment):
            if comment['replies'] != "":
                children = comment['replies']['data']['children']
                parse_children_for_comments(children)

def get_comments(url):
            req_data = requests.get(url, headers={'User-agent': userAgent})
            json_data = req_data.json()
            return json_data

def parse_children_for_comments(children):
            for child in children:
                diction = {}
                if child['kind'] == "more":
                    children = child['data']['children']
                if child['kind'] == "t1":
                    comment = child['data']['body']
                    user_id = child['data']['author']
                    
                    diction[user_id] = comment
                    if soccer_done_flag == False:
                        response_json = reddit_football_collection.insert_one(diction)
                    if soccer_done_flag and all_subreddits_done:
                        response_json = reddit_cricket_collection.insert_one(diction)
                    get_replies(child['data'])

while soccer_done_flag == False:
        lines = f.readlines()
        for i in range(len(lines)):
            line = lines[i]
            print("Subreddit name: ", line)
            res = authorize_me(line)
            print("Fetching soccer data...")
            for post in res.json()['data']['children']:
                post_count +=1
                #print("Post count: ", post_count)
                if post_count > 5:
                    post_count = 0

                    break         
                url = sanitize_input("https://www.reddit.com"+post['data']['permalink'])
                json_data = get_comments(url)
                for item in json_data:
                    children = item['data']['children']
                    parse_children_for_comments(children)
        print("Soccer data fetched.\n")
        all_subreddits_done = True
        soccer_done_flag = True


f = open("input_cricket.txt", "r")

post_count =0
while True:
        lines = f.readlines()
        for i in range(len(lines)):
            line = lines[i]
            print("Subreddit name: ", line)
            res = authorize_me(line)
            print("Fetching cricket data...")

            for post in res.json()['data']['children']:
                post_count +=1
                #print("Post count: ", post_count)
                if post_count > 5 :
                    post_count = 0
                    break
                url = sanitize_input("https://www.reddit.com"+post['data']['permalink'])
                json_data = get_comments(url)
                for item in json_data:
                    children = item['data']['children']
                    parse_children_for_comments(children)
            print("Cricket data fetched.\n")
        break
            
