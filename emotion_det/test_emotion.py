import numpy as np
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re
from tensorflow.keras.models import load_model
import joblib
from keras import backend as K

ps = PorterStemmer()

def preprocess(line):
    review = re.sub('[^a-zA-Z]', ' ', line)#leave characters only from a to z
    review = review.lower() #lower the text
    review = review.split() #turn the string into list of words
    #apply stemming
    review = [ps.stem(word) for word in review if not word in stopwords.words('english')] #delete stopwords like I,AND ,OR etc
    #turn list into sentence
    return " ".join(review)
	
def predict(text):
    le=joblib.load("./emotion_det/label_encoder.joblib")
    countv=joblib.load("./emotion_det/cv.joblib")
    K.clear_session()
    model=load_model("./emotion_det\\model.h5")
    text = preprocess(text)
    print(text)
    array = countv.transform([text]).toarray()
    pred = model.predict(array)
    del model
    a=np.argmax(pred, axis=1)
	#print(le.inverse_transform(a)[0])
    return le.inverse_transform(a)[0]


#result=predict('Ex Wife Threatening SuicideRecently I left')
#print("result:",result)