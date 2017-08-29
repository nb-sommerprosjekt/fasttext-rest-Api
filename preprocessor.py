import os
import re
import pickle
from langdetect import detect
from nltk.stem import snowball
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords




def text_to_clean_stemmed_text(tekst,pdf):
    norStem = snowball.NorwegianStemmer()
    with open('vocabulary.pickle', 'rb') as f:
        vocabulary=pickle.load(f)
    with open('vocabulary_stemmed.pickle', 'rb') as f:
        vocab_stemmed=pickle.load(f)
    if tekst != "":
        try:
            lang = detect(tekst)
        except Exception as e:
            return Exception("Noe gikk galt da vi prøvde å finne ut språket i teksten. Feilmeldingen er: ", e)


        if lang=="no":
            tekst = tekst.replace("-\n", "")
            # regexeses to remove all urls and emails
            tekst = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', "", tekst)
            tekst = re.sub(
                r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''',
                "", tekst)
            if pdf:
                #Done to fix incorrect word-splits from pfd converting
                lines = tekst.splitlines(True)
                lines = [x for x in lines if x != "\n"]
                for i in range(len(lines)):
                    if i < len(lines) - 1:
                        temp1 = lines[i].split(" ")
                        temp2 = lines[i + 1].split(" ")
                        word = temp1[-1] + temp2[0]
                        word = word.replace("\n", "")
                        word = word.lower()
                        word = re.sub('[^a-zA-ZæøåÆØÅ]+', ' ', word)
                        if word in vocabulary:
                            lines[i]=lines[i].replace("\n", "")
                        elif norStem.stem(word) in vocab_stemmed:
                            lines[i] =lines[i].replace("\n", "")
                        else:
                            lines[i] =lines[i].replace("\n", " ")
                temp = ""
                for line in lines:
                    temp += line + ""
                tekst = temp
            tekst = tekst.replace("\n", " ")
            tekst = tekst.lower()
            tekst = re.sub('[^a-zA-ZæøåÆØÅ]+', ' ', tekst)
            tekst = tekst.replace("  ", " ")

            tokens = word_tokenize(tekst)
            filtered_words = [word for word in tokens if word not in set(stopwords.words('norwegian'))]

            stemmed_words = list()
            for word in filtered_words:
                stemmed_words.append(norStem.stem(word))

            tekst = ' '.join(stemmed_words)

            return tekst
        else:
            return Exception("Teksten er ikke norsk, og kunnes derfor ikke testes.")
    else:
        return Exception("Teksten er tom.")

