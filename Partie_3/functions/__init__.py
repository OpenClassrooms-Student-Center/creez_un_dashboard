# -*- coding: utf-8 -*-
import re

def extract_keywords(texts):
    """
    Prends une liste de textes et en détecte les mots les plus fréquents. Cette fonction renvoie 
    la liste des textes et le comptage des mots.
    """

    keywords = {}
    articles = []

    for i, text in enumerate(texts):
        # Extraction des éléments selon la structure JSON renvoyée par l'API NEWSAPI.ORG
        source = text["source"]["name"]
        title = text["title"]
        description = text["description"]
        url = text["url"]
        content = text["content"]

        # Stockage des articles dans la variable articles
        articles.append({'title': title, 'url': url, 'source':source})

        # Détection des mots clés (mots les plus utilisés)
        text = str(title) + ' ' + str(description) + ' ' + str(content)
        words = normalise_and_get_words(text)

        # Comptage des mots
        for w in words :
            if w not in keywords:
                keywords[w] = {'cnt': 1, 'articles':[i]}
            else:
                keywords[w]['cnt'] += 1
                if i not in keywords[w]['articles']:
                    keywords[w]['articles'].append(i)

    # Tri des mots, du plus utilisé au moins utilisé
    keywords = [{'word':word, **data} for word,data in keywords.items()] 
    keywords = sorted(keywords, key=lambda x: -x['cnt'])

    return keywords, articles

def load_stop_words():
    """
    Charge la liste des stopwords français (les mots très utilisés qui ne sont pas porteurs de sens comme LA, LE, ET, etc.)
    """

    words = []
    # Ouverture du fichier "stop_words.txt"
    with open("stop_words.txt") as f:
        for word in f.readlines():
            words.append(word[:-1])
    return words

def normalise_and_get_words(text):
    """
    Prends un texte, le formate puis renvoie tous les mots significatifs qui le constituent
    """

    stop_words = load_stop_words()

    # Utilisation des expressions régulières (voir https://docs.python.org/3.7/library/re.html et https://openclassrooms.com/fr/courses/4425111-perfectionnez-vous-en-python/4464009-utilisez-des-expressions-regulieres)
    text = re.sub("\W"," ",text) # suppression de tous les caractères autres que des mots
    text = re.sub(" \d+", " ", text) # suppression des nombres
    text = text.lower() # convertit le texte en minuscules
    words = re.split("\s",text) # sépare tous les mots du texte

    words = [w for w in words if len(w) > 2] # suppression des mots de moins de 2 caractères
    words = [w for w in words if w not in stop_words] # suppression des stopwords
    return words