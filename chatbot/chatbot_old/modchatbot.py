from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pickle
import csv
import timeit
import random
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import nltk
import pandas as pd

def preprocess(sentence):
    sentence = sentence.lower()
    sentences = nltk.sent_tokenize(sentence.lower())
    words = nltk.word_tokenize(sentence.lower())
    new_words= [word for word in words if word.isalnum()]

    WordSet = []
    for word in new_words:
        if word not in set(stopwords.words("english")):
            WordSet.append(word)
        
    ps = PorterStemmer()    
    WordSetStem = []
    for word in WordSet:
        WordSetStem.append(ps.stem(word))
    
    lm= WordNetLemmatizer()
    WordSetLem = []
    for word in WordSet:
        WordSetLem.append(lm.lemmatize(word))
        
    sentence=""
    for i in WordSetLem:
        sentence+=i+" "
    return sentence

def train():
    csv_file_path = "randychat1111.csv"
    tfidf_vectorizer_pikle_path = "tfidf_vectorizer.pickle"
    tfidf_matrix_train_pikle_path = "tfidf_matrix_train.pickle"
    sentences = []
    df = pd.read_csv("new_dataset.csv")
    df.dropna(inplace=True)
    for i in df.iterrows():
        sentences.append(i[1][0])
    temp=[]
    for i in sentences:
        temp.append(preprocess(i))
    sentences=temp
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix_train = tfidf_vectorizer.fit_transform(sentences)
    f = open(tfidf_vectorizer_pikle_path, 'wb')
    pickle.dump(tfidf_vectorizer, f)
    f.close()
    f = open(tfidf_matrix_train_pikle_path, 'wb')
    pickle.dump(tfidf_matrix_train, f)
    f.close()
    print("Your chatbot has been trained successfully.")

def get_response(user_sentence):
    tfidf_vectorizer_pikle_path = "tfidf_vectorizer.pickle"
    tfidf_matrix_train_pikle_path = "tfidf_matrix_train.pickle"
    test_set = (user_sentence,"")
    temp=[]
    for i in test_set:
        temp.append(preprocess(i))
    test_set=temp
    f = open(tfidf_vectorizer_pikle_path, 'rb')
    tfidf_vectorizer = pickle.load(f)
    f.close()
    f = open(tfidf_matrix_train_pikle_path, 'rb')
    tfidf_matrix_train = pickle.load(f)
    f.close()
    tfidf_matrix_test = tfidf_vectorizer.transform(test_set)
    cosine = cosine_similarity(tfidf_matrix_test, tfidf_matrix_train)
    cosine = np
