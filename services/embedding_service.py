from sentence_transformers import SentenceTransformer
import psycopg2
from elasticsearch import Elasticsearch

model = SentenceTransformer("all-MiniLM-L6-v2")
es = Elasticsearch(["http://localhost:9200"])
db = psycopg2.connect(dbname="vector_db", user="user", password="pass", host="localhost")

def store_embeddings(text: str, doc_id: str):
    embeddings = model.encode([text])[0]
    with db.cursor() as cur:
        cur.execute("INSERT INTO embeddings (doc_id, vector) VALUES (%s, %s)",
                   (doc_id, embeddings.tolist()))
    db.commit()
    es.index(index="documents", id=doc_id, body={"text": text})
