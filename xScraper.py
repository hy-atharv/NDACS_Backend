from ntscraper import Nitter
import time

scraper = Nitter(log_level=1, skip_instance_check=False)


def disasterTweets():
    disasterTweetsData = []
    fTweetsData = []
    time.sleep(1)

    floodTweets = scrapeTweets("andhra pradesh flood")
    if len(floodTweets["tweets"]) > 0:
        for tweet in floodTweets["tweets"]:
            disasterTweetsData.append(tweet)

    # time.sleep(60)
    #
    # landslideTweets = scrapeTweets("landslide")
    # if len(landslideTweets["tweets"]) > 0:
    #     for tweet in landslideTweets["tweets"]:
    #         disasterTweetsData.append(tweet)
    #
    # time.sleep(60)
    #
    # cycloneTweets = scrapeTweets("cyclone")
    # if len(cycloneTweets["tweets"]) > 0:
    #     for tweet in cycloneTweets["tweets"]:
    #         disasterTweetsData.append(tweet)
    #
    # time.sleep(60)
    #
    # earthquakeTweets = scrapeTweets("earthquake")
    # if len(earthquakeTweets["tweets"]) > 0:
    #     for tweet in earthquakeTweets["tweets"]:
    #         disasterTweetsData.append(tweet)

    for tweet in disasterTweetsData:
        fTweetsData.append({
            "tweetLink": tweet["link"],
            "tweetText": tweet["text"],
            "tweetUser": tweet["user"],
            "tweetDate": tweet["date"],
            "tweetPicturesLinks": tweet["pictures"],
            "tweetVideosLinks": tweet["videos"],
            "tweetGifsLinks": tweet["gifs"]
        })

    print(fTweetsData)

    return fTweetsData

def scrapeTweets(disaster):
    try:
        tweets = scraper.get_tweets(disaster, mode="term", number=25, max_retries=2, since="2024-09-01", near="India", language="en")


        #disasterTweets = filterDisasterTweets(tweets)

        return tweets

    except:
        return{}


# def filterDisasterTweets(tweetsData):
#     tweets = tweetsData["tweets"]
#
#     disasterTweetsData = {}
#
#     floodTweets = []
#     landslideTweets = []
#     cycloneTweets = []
#     earthquakeTweets = []
#
#     for tweet in tweets:
#         if any(word in tweet["text"] for word in ["flood", "floods"]):
#             floodTweets.append(tweet)
#         elif any(word in tweet["text"] for word in ["landslide", "landslides"]):
#             landslideTweets.append(tweet)
#         elif any(word in tweet["text"] for word in ["cyclone", "cyclones"]):
#             cycloneTweets.append(tweet)
#         elif any(word in tweet["text"] for word in ["earthquake", "earthquakes"]):
#             earthquakeTweets.append(tweet)
#
#     disasterTweetsData = {
#         "floodTweets": floodTweets,
#         "landslideTweets": landslideTweets,
#         "cycloneTweets": cycloneTweets,
#         "earthquakeTweets": earthquakeTweets
#     }
# 
#     return disasterTweetsData

