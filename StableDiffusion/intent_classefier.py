import joblib
import numpy as np
from TextGeneration.memory import get_embedding

def load_model():
    global classifier
    classifier = joblib.load('classifier_checkpoint.joblib')

def classify_message(message):
    global classifier
    feature_vector = np.array(get_embedding(message))
    label = classifier.predict([feature_vector])[0]
    return label
