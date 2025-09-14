from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
from redis import Redis
import psycopg2
import numpy as np
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

model = SentenceTransformer("all-MiniLM-L6-v2")
es = Elasticsearch(["http://localhost:9200"])
redis_client = Redis(host="localhost", port=6379, db=0)
db = psycopg2.connect(dbname="vector_db", user="user", password="pass", host="localhost")

def hybrid_search(query: str, top_k: int):
    cache_key = f"search:{query}:{top_k}"
    cached = redis_client.get(cache_key)
    if cached:
        return cached.decode()

    es_results = es.search(index="documents", body={
        "query": {"match": {"text": query}},
        "size": top_k
    })

    query_embedding = model.encode([query])[0]
    with db.cursor() as cur:
        cur.execute("""
            SELECT doc_id, 1 - (vector <=> %s) as similarity 
            FROM embeddings 
            ORDER BY similarity DESC 
            LIMIT %s
        """, (query_embedding.tolist(), top_k))
        vector_results = cur.fetchall()

    combined_results = []
    es_ids = {hit["_id"]: hit["_score"] for hit in es_results["hits"]["hits"]}
    for doc_id, sim in vector_results:
        score = sim + (es_ids.get(doc_id, 0) * 0.5)
        combined_results.append({"doc_id": doc_id, "score": score})
    
    combined_results.sort(key=lambda x: x["score"], reverse=True)
    
    redis_client.setex(cache_key, 3600, str(combined_results[:top_k]))

    retriever = RetrievalQA.from_chain_type(
        llm=OpenAI(),
        chain_type="stuff",
        retriever=lambda x: [es.get(index="documents", id=r["doc_id"])["_source"]["text"] 
                           for r in combined_results[:top_k]]
    )
    rag_response = retriever.run(query)
    
    return {"results": combined_results[:top_k], "rag_response": rag_response}