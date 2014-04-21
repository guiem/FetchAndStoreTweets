# TwitterSearch params
CONSUMER_KEY = 'YOUR CONSUMER KEY'
CONSUMER_SECRET = 'YOUR CONSUMER SECRET'
ACCESS_TOKEN = 'YOUR ACCESS TOKEN'
ACCESS_TOKEN_SECRET = 'YOUR ACCESS TOKEN SECRET'
KEY_WORDS = ['word1','word2','wordN'] # check this URL to properly configure your Twitter search https://dev.twitter.com/docs/using-search (ie. exact phrase by using "exact phrase example" and combining it with OR expressions...)
UNTIL = False # set a datetime to filter tweets until the day you indicate

# TwitterTimeline params
TIMELINE_COUNT = 200
TIMELINE_KEYWORDS = ['word1','word2'] # but not expresions with OR

# DATABASE
DB_URL = 'localhost'

try:
    from settings_local import *
except:
    import traceback
    print traceback.print_exc()