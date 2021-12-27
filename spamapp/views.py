from django.shortcuts import render
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)
# Create your views here.
ps = PorterStemmer()

def home(request):
    return render(request,"index.html")
def detect(request):
    if request.method=='POST':
        email=request.POST['message']
        tfidf = pickle.load(open('vectorizer.pkl','rb'))
        model = pickle.load(open('model.pkl','rb'))
    # 1. preprocess
        transformed_sms = transform_text(email)
    # 2. vectorize
        vector_input = tfidf.transform([transformed_sms])
    # 3. predict
        result = model.predict(vector_input)[0]
    # 4. Display
        if result == 3:
            result="Spam"
        else:
            result="not a Spam!"
        return render(request,"index.html",context={'text':result,'content':email})
    else:
        return render(request,"index.html",{'text':""})