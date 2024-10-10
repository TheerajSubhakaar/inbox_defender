# classifier/views.py

from django.shortcuts import render
from .forms import TextInputForm
import joblib
import numpy as np
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from string import punctuation


svc_model = joblib.load('./models/SVC_model.pkl')
# knn_model = joblib.load('./models/KNN_model.pkl')
nb_model = joblib.load('./models/NB_model.pkl')
rf_model = joblib.load('./models/RF_model.pkl')
tfid = joblib.load('./models/tfidf_vectorizer.pkl')

models = [svc_model, nb_model, rf_model]
snowball_stemmer = SnowballStemmer(language='english')

# Text preprocessing function
def transform_text(text):
    tokens = word_tokenize(text.lower())

    processed_tokens = [
        snowball_stemmer.stem(token) for token in tokens
        if token.isalnum() and token not in stopwords.words('english') and token not in punctuation
    ]

    return " ".join(processed_tokens)

# Preprocess the input text
def preprocess_input(text):
    transformed_text = transform_text(text)
    return tfid.transform([transformed_text]).toarray()


def predict_ensemble(text):
    preprocessed_text = preprocess_input(text)
    predictions = [model.predict(preprocessed_text)[0] for model in models]
    final_prediction = 1 if np.sum(predictions) >= 3 else 0
    return "spam" if final_prediction == 1 else "ham"


def classify_message(request):
    result = None
    if request.method == 'POST':
        form = TextInputForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            result = predict_ensemble(message)
    else:
        form = TextInputForm()

    return render(request, 'classifier/classify.html', {'form': form, 'result': result})