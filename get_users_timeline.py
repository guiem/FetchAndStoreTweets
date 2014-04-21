from twitter import *
from settings import *
from utils import *
import pymongo
import datetime
import time

# user timeline https://dev.twitter.com/docs/api/1/get/statuses/user_timeline

def contains_keywords(tweet_text):
    for combo in TIMELINE_KEYWORDS:
        if combo in tweet_text:
            return True
    return False

t = Twitter(
            auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET,
                       CONSUMER_KEY, CONSUMER_SECRET)
            )

# connect to mongo
connection = pymongo.Connection("mongodb://{0}".format(DB_URL), safe=True)
db=connection.twitter
tweets = db.tweets
users = db.users

def get_timeline(screen_name, since_id = False):
    try:
        response = None
        if not since_id:
            response = t.statuses.user_timeline(screen_name=screen_name,count=TIMELINE_COUNT)
        else:
            response = t.statuses.user_timeline(screen_name=screen_name,count=TIMELINE_COUNT,since_id = since_id)
        count = 0
        next_max_id = 0
        todo = True
        new_since_id = 0
        while todo:
            todo = not (len(response) < TIMELINE_COUNT)
            for tweet in response:
                if contains_keywords(tweet['text'].encode('utf-8')) and tweets.find({"id":tweet['id'] }).count() == 0:
                    tweets.insert(tweet)
                count += 1
                tweet_id = tweet['id']
                if (tweet_id < next_max_id) or (next_max_id == 0):
                    next_max_id = tweet_id
                    next_max_id -= 1 # decrement to avoid seeing this tweet again
                new_since_id = max(new_since_id,tweet_id)
            if not since_id:
                response = t.statuses.user_timeline(screen_name=screen_name,count=TIMELINE_COUNT,max_id = next_max_id)
            else:
                response = t.statuses.user_timeline(screen_name=screen_name,count=TIMELINE_COUNT,since_id = since_id)
            sleep = needs_sleep(response.rate_limit_remaining,response.rate_limit_reset)
            if sleep:
                print 'Sleeping {0} seconds to avoid reaching rate limit.'.format(sleep)
                time.sleep(sleep)
        return new_since_id
    except Exception,e:
        print str(e)

users_processed = 0
users_updated = 0
for user in users.find():
    if 'since_id' in user.keys():
        users_updated += 1
    since_id = get_timeline(user['screen_name'], since_id = 'since_id' in user.keys() and user['since_id'])
    if since_id:
        users.update({"screen_name": user['screen_name']}, {"$set": {"processed": datetime.datetime.utcnow(),"since_id":since_id}})
    else:
        users.update({"screen_name": user['screen_name']}, {"$set": {"processed": datetime.datetime.utcnow()}})
    users_processed += 1
    print "{0}'s timline has been processed".format(user['screen_name'])
print 'Total users processed {0}. Users updated: {1}'.format(users_processed, users_updated)

