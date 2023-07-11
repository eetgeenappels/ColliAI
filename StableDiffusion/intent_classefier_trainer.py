import numpy as np
from sklearn.linear_model import LogisticRegression
from TextGeneration.memory import get_embedding
from TextGeneration.memory import load_model
from tqdm import tqdm
import joblib
import concurrent.futures
from threading import Lock

load_model()


# Define training data
with open('../draw.txt', 'r') as file:
    drawData = file.read().splitlines()

training_data = []

for drawText in drawData:
    training_data.append((drawText, "draw"))

with open('../not_draw.txt', 'r') as file:
    notDrawData = file.read().splitlines()

for notDrawText in notDrawData:
    training_data.append((notDrawText, "notdraw"))

# Preprocess training data and create feature vectors
X_train = []
y_train = []

# Create a lock for the shared counter
counter_lock = Lock()

# Initialize the shared counter
counter = 0

def process_data(data):
    global counter

    message, label = data
    feature_vector = get_embedding(message)
    np_array = np.array(feature_vector)

    with counter_lock:
        X_train.append(np_array)
        y_train.append(label)
        counter += 1

# Multithreading with ThreadPoolExecutor
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    for data in training_data:
        futures.append(executor.submit(process_data, data))

    # Create a tqdm progress bar with the total number of threads
    progress_bar = tqdm(total=len(training_data))

    # Check the completion of futures
    while counter < len(training_data):
        for future in concurrent.futures.as_completed(futures):
            future.result()

            # Update the progress bar
            with counter_lock:
                progress_bar.update()

            futures.remove(future)

# Close the progress bar
progress_bar.close()
print("did loading data")

# Train a logistic regression classifier
classifier = LogisticRegression()

print("created model")

classifier.fit(X_train, y_train)

print("finished training")

# Define a function to classify new messages
def classify_message(message):
    feature_vector = np.array(get_embedding(message))
    label = classifier.predict([feature_vector])[0]
    return label

# Test the classifier
test_messages = [
    "Can you draw a dog?",
    "What's the capital of France?",
    "Paint me a picture.",
    "How far is the moon?",
    "Design a website for me."
]

for message in test_messages:
    label = classify_message(message)
    print(f"Message: {message}\nClassification: {label}\n")

joblib.dump(classifier, 'classifier_checkpoint.joblib')