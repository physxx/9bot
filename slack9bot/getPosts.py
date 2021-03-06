import requests
from bs4 import BeautifulSoup
import json

#Dictionnaire des sections accèssible grâce au commandes de 9Bot
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
    '''
    Renvoie un string contenant l'aide des commandes possible avec 9Bot.
    '''
    str = "Command list :\t[section] [numberOfPosts]\nList of sections :"
    for s in sections:
        str += "\n" + "\t" + s
    return str

def getPage(section):
    '''
    Retourne le contenu HTML de la page 9gag de la section passée en paramètre.
    '''
    root = "http://9gag.com"
    url = root + section
    response = requests.get(url)
    return response

def getPostsOnPage(page, nbPost):
    '''
    Récupère le nombre de postes désiré passé de la page passé en paramètre.
    Le nb de postes sera arrondi à la dizaine supérieure. Retourne une liste de dictionnaire.
    Un dictionnaire contient les champs 'title', 'title_link' et 'image_url'.
    'title' est le titre du poste.
    'title_link' est le lien permettant d'accéder au poste.
    'image_url' est le lien de l'image du poste concerné.
    '''
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
    '''
    Vérifier si la commande existe.
    Si la commande est 'help' la fonction helpBot() est appelée et une liste contenant le string de l'aide sera retournée.
    Si la commande est valide et correspond à une section prise en compte par le bot, les fonctions getPage() et getPostsOnPage() seront appelées et une liste de json sera retournée.
    Les json contenus dans la liste sont un dump json des dictionnaires retournés par la fonction getPostsOnPage().
    Pour plus d'informations, sur la structure des dictionnaires contenus dans la liste voir la documentation de la fonction getPostsOnPage().
    Si la commande n'est pas valide, le string "Impossible de trouver la section [section]" sera le seul élément de la liste retournée.
    '''
    args = command.strip().split()
    msgs = []

    if(len(args) > 0):
        if args[0] == 'help':
            msgs.append(helpBot())
        else:
            section = args[0]
            nbPosts = 1
            if len(args) >= 2 :
                try:
                    nbPosts = int(args[1])
                except ValueError:
                    nbPosts = 1
                if nbPosts > 20:
                    nbPosts = 20

            if section in sections:
                page = getPage(sections[section])
                posts = getPostsOnPage(page, nbPosts)
                for p in posts[:nbPosts]:
                    msgs.append(json.dumps([p]))
            else:
                msgs.append("Impossible de trouver la section " + str(section))
    return msgs
