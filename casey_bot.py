import json
import tweepy
import config

# Set Twitter Auth Tokens
API_KEY = config.API_KEY
API_SECRET_KEY = config.API_SECRET_KEY
ACCESS_TOKEN = config.ACCESS_TOKEN
ACCESS_SECRET = config.ACCESS_SECRET

# Authenticate with the Twitter API via tweepy
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# Search for fitting Tweets
response = api.search(q="Casey weather la")

# Store Tweet IDs and Usernames from fitting Tweets
to_respond = []
for res in response:
    data = res._json
    tweet_id = data["id"]
    username = data["user"]["screen_name"]
    dictionary = {
        "tweet_id": tweet_id,
        "username": username,
                  }
    to_respond.append(dictionary)

# Load previously messaged Tweets
with open("masterlist.txt", "r") as master:
    masterlist = json.load(master)

# Send answers to fitting Tweets
for answer in to_respond:
    doubled_id = False
    tweet_id = answer["tweet_id"]
    username = answer["username"]
    status_text = f"@{username} - Please no more about the weather in L.A.! - yours faithfully, Casey"
    for i in range(len(masterlist)):
        if tweet_id == masterlist[i]["tweet_id"]:
            doubled_id = True
            print("Doubled ID")
    if not doubled_id:
        api.update_status(status=status_text, in_reply_to_status_id=tweet_id)
        print("Tweet send")

# Update previously messaged Tweets
with open("masterlist.txt", "w") as master:
    master.write(json.dumps(to_respond))
