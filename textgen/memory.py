import chromadb
from InstructorEmbedding import INSTRUCTOR
import json
from chromadb.config import Settings
from sklearn.metrics.pairwise import cosine_similarity

collection = None
model = None
client = None
count = -1
def create_database():
    global collection, client

    client = chromadb.Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory="database"
    ))
    
    collection = client.get_or_create_collection("chatlog", embedding_function=cosine_similarity)
    

def load_model():
    global model

    model = INSTRUCTOR('hkunlp/instructor-base')

def save_database():

    global collection, client

    client.persist()

def add_message(content):
    global collection

    # convert message to embedding
    embedding = model.encode(content).tolist()

    collection.add(
        embeddings = [embedding],

        metadatas = [
                {
                    "message_content": content
                }
            ],
        ids = [str(get_message_count())]
    )
    increment_message_count()

def get_embedding(text):
    return model.encode(text).tolist()

def get_message_count():
    with open("chat_metadata.json", "r") as f:
        return json.loads(f.read())["count"]
def increment_message_count():
    global count
    with open("chat_metadata.json", "r") as f:
        metadata = json.loads(f.read())
    metadata["count"] += 1
    count = metadata["count"]
    with open("chat_metadata.json", "w") as f:
        f.write(json.dumps(metadata))

def reset_db():
    client.delete_collection("chatlog")
    with open("chat_metadata.json", "w") as f:
        f.write('{"count": 0}')


def query(embedding):

    response = {
        "message_content": "",
        "id":-1
    }

    item = collection.query([embedding], n_results = 1) 

    response["message_content"] = item["metadatas"][0][0]["message_content"]
    response["id"] = int(item["ids"][0][0])

    return response

def get_last_n_messages(n):
    messages = []
    if get_message_count() == 0:
        print ("this is called")
        with open("chat_metadata.json", "r") as f:
            print(f.read())
        return []
    for i in range(get_message_count()-1, get_message_count()-1 - n, -1):
        if i < 0:
            break
        message = collection.get(ids=[str(i)])["metadatas"][0]["message_content"]
        messages.append(message)
    messages.reverse()
    return messages

def get_context(message_id):

    global collection
    def get_context_raw():
        if message_id == 0 and message_id == count-1:
            return [collection.get(ids=[str(message_id)])]
        if message_id == 0:
            return [collection.get(ids=[str(message_id)]), collection.get(ids=[str(message_id+1)])]
        if message_id == count-1:
            return [collection.get(ids=[str(message_id-1)]), collection.get(ids=[str(message_id)])]
        return [collection.get(ids=[str(message_id-1)]), collection.get(ids=[str(message_id)]), collection.get(ids=[str(message_id+1)])]
    context = get_context_raw()
    pure_text_context = []
    for message in context:
        pure_text_context.append(message["metadatas"][0]["message_content"])
    return pure_text_context
"""
Database Example

create_database()

reset_db()

create_database()
load_model()

add_message("Colli: Yo Colli")
add_message("You: How was your day?")
add_message("Colli: Good how was yours?")
add_message("You: great!")

save_database()

print(get_context(query(get_embedding("You: amazing!"))["id"]))
print(get_last_20_messages())
"""