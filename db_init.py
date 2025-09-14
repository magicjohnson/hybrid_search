import psycopg2

def init_db():
    db = psycopg2.connect(dbname="vector_db", user="user", password="pass", host="localhost")
    with db.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS embeddings (
                doc_id TEXT PRIMARY KEY,
                vector VECTOR(384)
            )
        """)
    db.commit()
    db.close()