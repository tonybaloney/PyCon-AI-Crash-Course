import numpy as np
import json
from openai import OpenAI
from utils import OLLAMA_URL


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """
    Calculate the cosine similarity between two vectors
    """
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def get_model_embedding(client, text, model="nomic-embed-text", dimensions=1024):
    response = client.embeddings.create(
        input=text,
        model=model,
        dimensions=dimensions, # default is 1536 for text-embedding-3-small. Is not an arbitrary number, is one of the accepted values (256, 512, 1024)
    )
    return response.data[0].embedding

def seed_embeddings_json():
    with open("data/clothes.json", "r") as f:
        data = json.load(f)

    client = OpenAI(
        base_url=OLLAMA_URL,
        api_key='api_key',
    )

    for item in data:
        item["embedding_nomic"] = get_model_embedding(client, model='nomic-embed-text', text=item["name"] + ' ' + item["description"])
        item['embedding_granite'] = get_model_embedding(client, model='granite-embedding:278m', text=item["name"] + ' ' + item["description"])
        print('.', end='')
    
    with open("data/clothes.json", "w") as f:
        json.dump(data, f, indent=4)
    
    print("Embeddings saved to clothes_embeddings.json")
