# ai/build_knowledge.py
from ai.rag import build_vector_db_from_txt

if __name__ == "__main__":
    build_vector_db_from_txt("ai/knowledge.txt")  # or "data/knowledge.txt"
    print("✅ Vector DB built from knowledge.txt")
