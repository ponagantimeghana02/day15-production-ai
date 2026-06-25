from fastapi import FastAPI
import chromadb

app = FastAPI(title="RAG Service")

client = chromadb.PersistentClient(path="./vector_db")

collection = client.get_or_create_collection(
    name="documents"
)

@app.get("/")
def root():
    return {
        "service": "rag",
        "status": "running"
    }

@app.post("/add")
def add_document():
    collection.add(
        documents=["FastAPI is a modern web framework"],
        ids=["1"]
    )

    return {"message": "document added"}

@app.get("/search")
def search():
    result = collection.query(
        query_texts=["FastAPI"],
        n_results=1
    )

    return result