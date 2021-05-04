from flask import Flask,redirect, url_for, render_template,request, session
from bs4 import BeautifulSoup as soup
import string
import requests

from website import create_app
#Create a instance of flask application
app = create_app()

'''
@app.route("/")
def home():
    return render_template("index.html")
'''
'''
@app.route("/", methods=["POST", "GET"])
def getInput():
    if request.method == 'POST':
        #Retrieve the seraching target
        aim = request.form['content']
        #Store it in session
        session["content"] = aim
        return redirect(url_for("scrape"))
    else:
        return render_template("search.html")

@app.route("/scrape", methods=["POST", "GET"])
def scrape():
    if request.method == 'POST':
        language = request.form['language']
        session["language"] = language
        return redirect(url_for("transform"))
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
                    

        return render_template("scrape.html", key=headers, val=details, content=info)


@app.route("/<name>")
#The name in the url will pass into the function
def user(name):
    return  f"Hello {name}"

@app.route("/admin")
def admin():
    #return redirect(url_for("home"))
    return redirect(url_for("user", name="kevin"))


@app.route("/transform")
def transform():
    if "language" in session:
        language = session["language"]
        return render_template("transform.html", language=language)
    else:
        return redirect(url_for("scrape"))
'''


if __name__ == "__main__":
    app.run(debug=True)