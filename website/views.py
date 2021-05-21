from flask import Flask,redirect, url_for, render_template,request, session, Blueprint
from bs4 import BeautifulSoup as soup
import string
import requests
import wikipedia
import json
from pprint import pprint


from wikipedia.wikipedia import summary


#from transformer into translate

views = Blueprint('views', __name__)
global dataset
inputData = {}
infobox={}
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
        capWords = string.capwords(content)
        wordList = capWords.split()
        content = "_".join(wordList)

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
        #Fulfill the summary of specific content
        search_result = wikipedia.page(wikipedia.search(content)[0])
        inputData["summary"] = search_result.summary
        inputData["path"] = "C:\OSU\CS361\WebScrapper\input.json"

        dataset = infobox
        print(dataset)
        session["info"] = infobox
        session["headers"] = headers
        session["input"] = inputData
        #Converts info to json format
        json_content = json.dumps(infobox, indent=len(infobox))
        json_input = json.dumps(inputData, indent=len(inputData))
        #Transfer infobox
        with open("scrape.json", "w") as f:
            f.write(json_content)

        #Transfer paragraphs to Michille
        with open("input.json", "w") as f:
            f.write(json_input)
        return render_template("scrape.html",  content=infobox, part=section, summary=inputData["summary"])


'''
@app.route("/<name>")
#The name in the url will pass into the function
def user(name):
    return  f"Hello {name}"

@app.route("/admin")
def admin():
    #return redirect(url_for("home"))
    return redirect(url_for("user", name="kevin"))
'''

@views.route("/transform", methods=["POST", "GET"])
def transform():
    if request.method == "POST":
        if "language" in session:
            language = session["language"]
            headers = session["headers"]
            info = session["info"]
            '''
            summary = session["summary"]

            summary.update({"language": language})
            json_language = json.dumps(summary, indent=len(summary))
            with open("input.json", "w") as f:
                f.write(json_language)
            '''
            
            #Translate in the backend
            #Support other language
            with open("output.txt", "r", encoding="utf8") as f:
                #Retrieve scraping data(dictionary)
                content = f.read()

            #Insert translate function to translate info/content/dataset
            



            return render_template("transform.html", language=language,  content=content)
        else:
            return redirect(url_for("views.scrape"))

