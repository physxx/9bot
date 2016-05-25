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
            "nsfw" : "/nsfw", "nsfwHot" : "/nsfw/hot", "nsfwFresh" : "/nsfw/fresh"}

class Post:
    def __init__(self, postId, postTitle, postLink, postImgLink):
        self.id = postId
        self.title = postTitle
        self.link = postLink
        self.ImageLink = postImgLink

    def __str__(self):

        return str(self.id) + "\n" + str(self.title) + "\n" + str(self.link) + "\n" + str(self.ImageLink)

def helpBot():
    print("Command list :")
    print("\t[section]")
    print("\nList of sections :")
    for s in sections:
        print ("\t" + s)

def getPosts(section, nbPost):
    root = "http://9gag.com"
    url = root + section
    gagLink = ""
    gagRoot = "http://9gag.com/gag/"

    maxCount = nbPost #Par 10
    count = 0

    response = requests.get(url)
    htmlData = response.content
    pageSoup = BeautifulSoup(htmlData, "lxml")
    articles = pageSoup.find_all("article")

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

            p = Post(gagID, gagTitle, gagLink, gagData)
            posts.append(p)
        next = pageSoup.find_all("div",{"class" : "loading"})
        url = root + next[0].a['href']

        # Next 10 articles
        response = requests.get(url)
        htmlData = response.content
        pageSoup = BeautifulSoup(htmlData, "lxml")
        articles = pageSoup.find_all("article")

    return posts

def checkCommand(command):
    args = command.strip().split()

    if(len(args) > 0):
        if args[0] == 'help':
            helpBot()
        else:
            section = args[0]
            nbPosts = 1
            if len(args) >= 2 :
                nbPosts = int(args[1])

            if section in sections:
                print("La section " + section + " existe")
                print(sections[section])
                posts = getPosts(sections[section], nbPosts)
                p = iter(posts)
                for _ in range(nbPosts):
                    print(str(next(p)) + "\n")
            else :
                print ("Impossible de trouver la section ", str(section))
    else:
        print("ne rien faire") #Ce cas n'arrivera pas avec Slack car impossible d'envoyer des messages vides

command = input("Entrer sections: ")
checkCommand(command)
