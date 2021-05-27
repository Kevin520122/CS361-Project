from flask import Flask,redirect, url_for, render_template,request, session, Blueprint
from bs4 import BeautifulSoup as soup
import string
import requests
import wikipedia
import json
from pprint import pprint
from website import format


from wikipedia.wikipedia import summary


#from transformer into translate

views = Blueprint('views', __name__)
#Global variables
global dataset
inputData = {}
infobox={}
images={}
cars = {}


#@views.route('/')
@views.route("/", methods=["POST", "GET"])
def getInput():
    if request.method == 'POST':
        #Retrieve the seraching target
        aim = request.form['content']
        section = request.form["section"]
        session["section"] = section
        #Store it in session
        session["content"] = aim
        return redirect(url_for("views.scrape"))
    else:
        return render_template("search.html")

@views.route("/home")
def displayHome():
    return render_template("home.html")

@views.route("/car", methods=["POST", "GET"])
def car():
    if request.method == 'POST':
        session["car"] = request.form["car"]
        return redirect(url_for("views.scrape_car"))
    else:
        return render_template("car.html")

@views.route("/scrape_car", methods=["POST", "GET"])
def scrape_car():
    if request.method == "POST":
        pass
    else:
        if "car" in session:
            brand = session["car"]
        else:
            return redirect(url_for("car"))

        brand = format.formatStr(brand)
        wikiURL = "https://en.wikipedia.org/wiki/"+brand
        data = requests.get(wikiURL)
        #Returns an array containing all the html code
        contents = soup(data.content, "html.parser")
        #Returns an array containing infobox html code
        info = contents("td", {"class":"infobox-image"})[0]
        #print(info)
        img = info.find_all("img")[0]
    

        cars["path"] = "C:\OSU\CS361\WebScrapper\car.json"
        cars["img"] = "https:"+img["src"]
        cars["brand"] = brand

        json_car = json.dumps(cars, indent=len(cars))
        with open("car.json", "w") as f:
            f.write(json_car)

        return render_template("scrape_car.html", name=brand, img=cars["img"])
        



@views.route("/scrape", methods=["POST", "GET"])
def scrape():
    if request.method == 'POST':
        language = request.form['language']
        session["language"] = language
        

        inputData.update({"language": language})
        json_language = json.dumps(inputData, indent=len(inputData))
        with open("input.json", "w") as f:
            f.write(json_language)
    
        return render_template("scrape.html", part = session["section"], summary=inputData["summary"], content=infobox, language=language)

    else:
        #section = request.form["section"]
        
        content = ""
        if "content" in session and "section" in session:
            content = session["content"]
            section = session["section"]
        else:
            return redirect(url_for("getInput"))
        
        #Clean and format the content
        #format.formatStr(content)
        '''
        capWords = string.capwords(content)
        wordList = capWords.split()
        content = "_".join(wordList)
        
        '''

        '''
        wikiURL = "https://en.wikipedia.org/wiki/"+content
        data = requests.get(wikiURL)
        #print(data)
        #Returns an array containing all the html code
        contents = soup(data.content, "html.parser")
        #Returns an array containing infobox html code
        info = contents("table", {"class":"infobox"})[0]
        #print(info)

        rows = info.find_all('tr')

        headers = []
        details = []
        
        

        for row in rows:
            headersHTML = row.find_all('th')
            
            detailsHTML = row.find_all('td')

            if headersHTML is not None and detailsHTML is not None:
                for header, detail in zip(headersHTML, detailsHTML):
                    headers.append(header.text)
                    details.append(detail.text)
                    info[header.text] = detail.text
        '''

        #Get all the content for Wikipedia
        search_result = wikipedia.page(wikipedia.search(content)[0])
        #Fulfill the summary of specific content
        inputData["summary"] = search_result.summary
        inputData["path"] = "C:\OSU\CS361\WebScrapper\input.json"

        images["links"] = search_result.images
        images["path"] = "C:\OSU\CS361\WebScrapper\image.json"

    
        session["input"] = inputData
        #Converts info to json format
        
        json_input = json.dumps(inputData, indent=len(inputData))
        json_image = json.dumps(images, indent=len(images))
        
        #Transfer paragraphs to Michille
        with open("input.json", "w") as f:
            f.write(json_input)

        #Transfer images
        with open("image.json", "w") as f:
            f.write(json_image)
        return render_template("scrape.html",   part=section, summary=inputData["summary"], images=images["links"])



@views.route("/transform", methods=["POST", "GET"])
def transform():
    if request.method == "POST":
        if "language" in session:
            language = session["language"]
            headers = session["headers"]
            info = session["info"]
            
            
            
            #Translate in the backend
            #Support other language
            with open("output.txt", "r", encoding="utf8") as f:
                #Retrieve scraping data(dictionary)
                content = f.read()

            #Insert translate function to translate info/content/dataset
            



            return render_template("transform.html", language=language,  content=content)
        else:
            return redirect(url_for("views.scrape"))

