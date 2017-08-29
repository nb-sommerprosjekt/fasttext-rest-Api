import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask_cors import CORS
from html2text import html2text

import classifier

app = Flask(__name__)
CORS(app)


@app.route('/rest_doc/<path:url>', methods = ['GET', 'POST'])
def read_text_url(url):

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
    return res


if __name__ == '__main__':
    app.run(debug = True)

