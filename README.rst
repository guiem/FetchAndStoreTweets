*******************
FetchAndStoreTweets
*******************
1. Searches for users that have tweeted specific key words and stores them in a mongodb database.
2. Retrieves all users' timelines filtering tweets containing that specific keywords.

This two separeted phases are due to a constraint in Twitter's search API. It only gives you tweets until about 7 days in the past, and I wanted to retrieve all tweets containing a specific keyword.
So I'm just reading their timelines (it lets to retrieve about 3200 tweets, which may not be enough as well, I know).

Just built this for personal use, so I didn't care about creating an extensive documentation.
But, please, please, if you think you might want to use this code do not hesitate in emailing me and I'll write a propper documentation. Specially about what is this code intended to do.
My e-mail: g@guiem.info
