import requests
from bs4 import BeautifulSoup
import json

sections = {"hot" : "/hot", "trending" : "/trending", "fresh" : "/fresh",
            "geeky" : "/geeky", "geekyHot" : "/geeky/hot", "geekyFresh" : "/geeky/fresh",
            "wtf" : "/wtf", "wtfHot" : "/wtf/hot", "wtfFresh" : "/wtf/fresh",
            "funny" : "/funny", "funnyHot" : "/funny/hot", "funnyFresh" : "/funny/fresh",
            "meme" : "/meme", "memeHot" : "/meme/hot", "memeFresh" : "/meme/fresh",
            "cute" : "/cute", "cuteHot" : "/cute/hot", "cuteFresh" : "/cute/fresh",
            "comic" : "/comic", "comicHot" : "/comic/hot", "comicFresh" : "/comic/fresh",
            "food" : "/food", "foodHot" : "/food/hot", "foodFresh" : "/food/fresh",
            "timely" : "/timely", "timelyHot" : "/timely/hot", "timelyFresh" : "/timely/fresh",
            "design" : "/design", "designHot" : "/design/hot", "designFresh" : "/design/fresh",
            "gif" : "/gif", "gifHot" : "/gif/hot", "gifFresh" : "/gif/fresh",
            "cosplay" : "/cosplay", "cosplayHot" : "/cosplay/hot", "cosplayFresh" : "/cosplay/fresh",
            "girl" : "/girl", "girlHot" : "/girl/hot", "girlFresh" : "/girl/fresh",
            "nsfw" : "/nsfw", "nsfwHot" : "/nsfw/hot", "nsfwFresh" : "/nsfw/fresh",
            "random" : "/random"}

def helpBot():
    print("Command list :")
    print("\t[section]")
    print("\nList of sections :")
    for s in sections:
        print ("\t" + s)

def getPage(section):
    root = "http://9gag.com"
    url = root + section
    response = requests.get(url)
    return response

def getPostsOnPage(page, nbPost):
    root = "http://9gag.com"
    gagLink = ""
    gagRoot = "http://9gag.com/gag/"
    htmlData = page.content
    pageSoup = BeautifulSoup(htmlData, "lxml")
    articles = pageSoup.find_all("article")

    maxCount = nbPost #Par 10
    count = 0

    posts = []

    while (count<maxCount):
        for article in articles:
            gagID = article.get("data-entry-id")

            gagTitle = article.h2.text.strip()

            if gagID is not None:
                gagLink = gagRoot + gagID
                count = count +1
            # Add gagData
            try:
                # GIF image
                gagData = article.div.a.div['data-image']
            except:
                try:
                    #JPG file
                    gagData = article.div.a.img['src']

                    if "460c" in gagData and gagID is not None:
                        gagData = imgRoot + gagID +"_700b.jpg"
                    else:
                        gagData = gagData.replace("460s","700b")

                except :
                    # NSFW Image
                    if gagID is not None:
                        gagData = "http://ultimate.best9gagclonescript.com/styles/light/img/nsfw.jpg"

            p = {"title": gagTitle ,"title_link": gagLink ,"image_url": gagData}
            posts.append(p)
        next = pageSoup.find_all("div",{"class" : "loading"})
        url = root + next[0].a['href']

        # Next 10 articles
        page = requests.get(url)
        htmlData = page.content
        pageSoup = BeautifulSoup(htmlData, "lxml")
        articles = pageSoup.find_all("article")

    return posts

def checkCommand(command):
    args = command.strip().split()
    msgs = []

    if(len(args) > 0):
        if args[0] == 'help':
            helpBot()
        else:
            section = args[0]
            nbPosts = 1
            if len(args) >= 2 :
                nbPosts = int(args[1])

            if section in sections:
                page = getPage(sections[section])
                posts = getPostsOnPage(page, nbPosts)
                for p in posts[:nbPosts]:
                    msgs.append(json.dumps([p]))
            else :
                msgs.append("Impossible de trouver la section " + str(section))

    return msgs

command = input("Entrer sections: ")
posts = checkCommand(command)
for p in posts:
    print(p)
