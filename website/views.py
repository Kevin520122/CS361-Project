from flask import Flask,redirect, url_for, render_template,request, session, Blueprint
from bs4 import BeautifulSoup as soup
import string
import requests

#from transformer into translate

views = Blueprint('views', __name__)
global dataset
dataset = {}
#@views.route('/')
@views.route("/", methods=["POST", "GET"])
def getInput():
    if request.method == 'POST':
        #Retrieve the seraching target
        aim = request.form['content']
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
        return redirect(url_for("views.transform"))
    else:
    
        content = ""
        if "content" in session:
            content = session["content"]
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
        info = {}

        for row in rows:
            headersHTML = row.find_all('th')
            
            detailsHTML = row.find_all('td')

            if headersHTML is not None and detailsHTML is not None:
                for header, detail in zip(headersHTML, detailsHTML):
                    headers.append(header.text)
                    details.append(detail.text)
                    info[header.text] = detail.text
                    
        dataset = info
        print(dataset)
        session["info"] = info
        session["headers"] = headers
        return render_template("scrape.html", key=headers, val=details, content=info)

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

@views.route("/transform")
def transform():
    if "language" in session:
        language = session["language"]
        headers = session["headers"]
        info = session["info"]
        #Insert translate function to translate info/content/dataset
        return render_template("transform.html", language=language, headers=headers, content=info)
    else:
        return redirect(url_for("views.scrape"))

