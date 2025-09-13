import pickle
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline

# Load embeddings
try:
    with open("index/embeddings.pkl", "rb") as f:
        data = pickle.load(f)
except FileNotFoundError:
    print("❌ No embeddings found. Run build_index.py first.")
    exit()

texts = data["texts"]
embeddings = data["embeddings"]

# Load models
embedder = SentenceTransformer("all-MiniLM-L6-v2")
qa_model = pipeline("text2text-generation", model="google/flan-t5-base")  # better than small

def answer_question(question):
    # Find most similar text chunks
    q_emb = embedder.encode(question, convert_to_tensor=True)
    hits = util.semantic_search(q_emb, embeddings, top_k=5)  # retrieve top 5
    context = " ".join([texts[hit['corpus_id']] for hit in hits[0]])

    # Generate answer
    result = qa_model(
        f"Answer the question based on context:\nQuestion: {question}\nContext: {context}"
    )
    return result[0]['generated_text']

if __name__ == "__main__":
    print("🤖 Chatbot ready! Type 'exit' to quit.")
    while True:
        q = input("You: ")
        if q.lower() == "exit":
            break
        print("Bot:", answer_question(q))
