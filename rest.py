import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask_cors import CORS
from html2text import html2text

import classifier
import preprocessor
import time
app = Flask(__name__)
CORS(app)

@app.route('/rest_doc/<path:url>', methods = ['GET'])
def read_text_url(url):
    start = time.time()
    log_file = open("log_file.txt", "a")

    url = url.replace("%3A",":")
    url_decoded = url.replace("%2F","/")

    r = requests.get(url_decoded)
    soup = BeautifulSoup(r.text)
    streng = soup.get_text()
    streng.encode('utf8')
    clean = html2text(streng)
    test_string="Penger er kult, og finans og poteter"
    #res =classifier.run_classification(str(clean))
    res = classifier.run_classification(clean)
    total_time = time.time()- start
    log_file.write("url:::"+str(url_decoded)+"\n"+"\n" +
                   str(res)+"\n"+"\n"
                   +"Tid brukt:"+str(total_time)+"\n"+"\n"
                   +"Tekst brukt til klassifisering:"+'\n'+'\n'
                   +str(preprocessor.text_to_clean_stemmed_text(streng,False)))

    return res





if __name__ == '__main__':
    app.run(debug = True)

