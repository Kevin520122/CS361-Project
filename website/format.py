import string
def formatStr(content):
    capWords = string.capwords(content)
    wordList = capWords.split()
    content = "_".join(wordList)
    return content