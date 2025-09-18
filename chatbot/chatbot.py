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
qa_model = pipeline("text2text-generation", model="google/flan-t5-base")

# Predefined chit-chat responses
smalltalk_responses = {
    "hi": "Hello! 👋 How can I help you today?",
    "hello": "Hi there! 😊 What would you like to know?",
    "hey": "Hey! 🙌 Ask me anything.",
    "how are you": "I’m just a bot, but I’m doing great! Thanks for asking. How are you?",
    "who are you": "I’m your friendly chatbot assistant. 🤖",
    "bye": "Goodbye! 👋 Have a great day!"
}

def answer_question(question):
    # Check for small-talk (lowercase matching)
    q_lower = question.lower().strip()
    for key, reply in smalltalk_responses.items():
        if key in q_lower:
            return reply

    # Otherwise → knowledge-based answer
    q_emb = embedder.encode(question, convert_to_tensor=True)
    hits = util.semantic_search(q_emb, embeddings, top_k=5)
    context = " ".join([texts[hit['corpus_id']] for hit in hits[0]])

    result = qa_model(
        f"You are the student assistance and helping their query:\nQuestion: {question}\nContext: {context}"
    )
    return result[0]['generated_text']

if __name__ == "__main__":
    print("🤖 Chatbot ready! Type 'exit' to quit.")
    while True:
        q = input("You: ")
        if q.lower() == "exit":
            break
        print("Bot:", answer_question(q))
