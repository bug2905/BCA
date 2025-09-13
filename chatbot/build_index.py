import os
import glob
import pandas as pd
import pickle
from sentence_transformers import SentenceTransformer

def chunk_text(text, chunk_size=300):
    """Split text into smaller chunks (for better embeddings)"""
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

if __name__ == "__main__":
    # Load all scraped CSVs
    files = glob.glob("data/*.csv")
    texts = []
    for file in files:
        df = pd.read_csv(file)
        for content in df["content"].tolist():
            texts.extend(chunk_text(content))

    if not texts:
        print("❌ No scraped data found. Run scraper.py first.")
        exit()

    # Build embeddings
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(texts, convert_to_tensor=True)

    # Save embeddings + texts
    os.makedirs("index", exist_ok=True)
    with open("index/embeddings.pkl", "wb") as f:
        pickle.dump({"texts": texts, "embeddings": embeddings}, f)

    print("✅ Embeddings built and saved in index/embeddings.pkl")
