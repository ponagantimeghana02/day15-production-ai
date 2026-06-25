from fastapi import FastAPI
import redis
import psycopg2
import os

app = FastAPI(title="AI API Service")

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "api"
    }

@app.get("/redis-test")
def redis_test():
    try:
        r = redis.Redis(host=REDIS_HOST, port=6379)
        r.set("message", "Redis Connected")
        value = r.get("message").decode()
        return {"redis": value}
    except Exception as e:
        return {"error": str(e)}

@app.get("/postgres-test")
def postgres_test():
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            database="aidb",
            user="admin",
            password="admin123"
        )
        conn.close()
        return {"postgres": "connected"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def root():
    return {"message": "AI API Running"}