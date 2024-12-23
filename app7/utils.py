# recommendations/utils.py
# recommendations/utils.py
import pandas as pd
import numpy as np
import re
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Load the dataset
def load_data(filepath):
    data = pd.read_csv(filepath)
    data.dropna(inplace=True)  # Drop rows with missing values
    data.drop('Unnamed: 0', inplace=True, axis=1)  # Drop any unnamed columns
    return data

# Data cleaning and preprocessing functions
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s,]', '', text)
    text = re.sub(r'\b(?:lb|tsp|tbsp|total|cup|cups|oz|teaspoons|teaspoon)\b', '', text)
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    return ' '.join(words)

def stem(text):
    ps = PorterStemmer()
    return " ".join([ps.stem(word) for word in text.split()])

def lemm(text):
    lm = WordNetLemmatizer()
    return " ".join([lm.lemmatize(word) for word in text.split()])

def preprocess_data(data):
    data["Cleaned_Ingredients"] = data["Ingredients"].apply(clean_text)
    data["Cleaned_Ingredients"] = data["Cleaned_Ingredients"].apply(stem)
    data["Cleaned_Ingredients"] = data["Cleaned_Ingredients"].apply(lemm)
    return data

def get_recipe_vectors(data):
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(data["Cleaned_Ingredients"]).toarray()
    return cv, vectors

def calculate_similarity(vectors):
    return cosine_similarity(vectors)
