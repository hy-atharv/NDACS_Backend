from gnews import GNews
from newspaper import Article
import time
import datetime
from googlenewsdecoder import decoderv3
from newsSourceLinks import scrapedLinks

#google_news = GNews(language='en', country='IN', max_results=10, start_date=(2024,8,1), end_date=(2024,8,30))



def disasterNews():
    disasterNewsData = []
    time.sleep(5)

    newsLinks = scrapedLinks("floods news India")
    floodNewsData = getNewsData(newsLinks)
    if len(floodNewsData) > 0:
        for article in floodNewsData:
            disasterNewsData.append(article)

    time.sleep(5)

    newsLinks = scrapedLinks("landslide news India")
    landslideNewsData = getNewsData(newsLinks)
    if len(landslideNewsData) > 0:
        for article in landslideNewsData:
            disasterNewsData.append(article)

    time.sleep(5)

    newsLinks = scrapedLinks("cyclone news India")
    cycloneNewsData = getNewsData(newsLinks)
    if len(cycloneNewsData) > 0:
        for article in cycloneNewsData:
            disasterNewsData.append(article)

    time.sleep(5)

    newsLinks = getNewsData("earthquake news India")
    earthquakeNewsData = getNewsData(newsLinks)
    if len(earthquakeNewsData) > 0:
        for article in earthquakeNewsData:
            disasterNewsData.append(article)

    print(disasterNewsData)

    articlesData = []

    for article in disasterNewsData:
        articlesData.append({
            "articleSourceURL": article["articleSourceURL"],
            "articleTitle": article["articleTitle"],
            "articleText": article["articleText"],
            "articleDate": article["articleDate"],
            "articleTime": article["articleTime"],
            "articleTopImage": article["articleTopImage"]
        })

    return articlesData

def getNewsData(links):
    newsData = scrapeNewsData(links)
    if len(newsData) > 0:
        return newsData
    else:
        return []


# def floodNews():
#     newsData = getNewsData("flood")
#     if len(newsData) > 0:
#         return newsData
#     else:
#         return None
#
# def landslideNews():
#     newsData = getNewsData("landslide")
#     if len(newsData) > 0:
#         return newsData
#     else:
#         return None
#
# def cycloneNews():
#     newsData = getNewsData("cyclone")
#     if len(newsData) > 0:
#         return newsData
#     else:
#         return None
#
# def earthquakeNews():
#     newsData = getNewsData("earthquake")
#     if len(newsData) > 0:
#         return newsData
#     else:
#         return None
#
#
# def getNewsData(disaster):
#
#         responses = google_news.get_news(disaster)
#         scrapedData = scrapeNewsData(responses)
#         return scrapedData
#





def scrapeNewsData(links):
    articles = []
    for link in links:

        try:

            # # Decoding Google News Links
            # google_url = response['url']
            # print(google_url)
            # decoded_url = decoderv3(google_url)
            # print(decoded_url)
            # actual_url = decoded_url["url"]
            # Scraping Article
            article = Article(link)
            article.download()
            article.parse()

            a = article.publish_date
            # Convert date and time to strings
            articleDate = a.strftime("%Y-%m-%d")  # Converts to '2024-08-06'
            articleTime = a.strftime("%H:%M:%S")  # Converts to '06:34:32'



            # Storing Data
            articles.append({
            "articleSourceURL": link,
            "articleDate": articleDate,
            "articleTime": articleTime,
            "articleAuthors": article.authors,
            "articleTitle": article.title,
            "articleText": article.text,
            "articleTopImage": article.top_image
            })

        except:
            print("Couldnt scrape article")



    return articles



