import numpy as np
import json
from openai import OpenAI
from utils import OLLAMA_URL
import utils
import pandas as pd

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


def get_embedding_client() -> tuple[OpenAI, int, str]:
    """
    Get the client, dimensions, and model for the embedding API.
    """

    api_key = utils.get_api_key()

    if utils.MODE == "github":
        model = "text-embedding-3-small"  # A fast, small model
        base_url = "https://models.inference.ai.azure.com"
        dimensions = 1024 # default is 1536 for text-embedding-3-small. Is not an arbitrary number, is one of the accepted values (256, 512, 1024, etc.)
    elif utils.MODE == "ollama":
        # pick which one works for you
        # model = "nomic-embed-text"  # A comparable open-source model
        model = "granite-embedding:278m"  # a multilingual model
        base_url = utils.get_base_url()
        dimensions = 768  # Both granite and nomic-embed-text have 768 dimensions
    else:
        raise ValueError("Invalid mode. Please set MODE to 'ollama' or 'github'.")

    # OpenAI client is a class. The old API used to use globals. Sometimes you might see code snippets for the old API. 

    client = OpenAI(
        base_url=base_url,
        api_key=api_key,
    )
    return client, dimensions, model

def get_embedding(client: OpenAI, dimensions: int, model: str, input:str) -> list[float]:
    """
    Get the embedding for the input text.
    """
    response = client.embeddings.create(
        input=input,
        model=model,
        dimensions=dimensions,
    )
    return response.data[0].embedding


def load_clothing_data(model: str) -> pd.DataFrame:
    data = pd.read_json("data/clothes.json")
    if utils.MODE == "ollama":
        if model == "nomic-embed-text":
            data['embedding'] = data.embedding_nomic
        elif model == "granite-embedding:278m":
            data['embedding'] = data.embedding_granite
        else:
            raise ValueError("I didn't precompute those embeddings. ")

    return data