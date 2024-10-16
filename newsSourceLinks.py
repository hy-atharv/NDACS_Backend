from googlesearch import search



def scrapedLinks(query):
    links = []
    for j in search(query, tld="com", num=20, stop=20, pause=10):
        print(j)
        links.append(j)

    return links

print(scrapedLinks("Coughing"))