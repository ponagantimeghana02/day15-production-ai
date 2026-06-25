from fastapi import FastAPI

app = FastAPI(title="AI Agent Service")

@app.get("/")
def root():
    return {
        "service": "agent",
        "status": "running"
    }

@app.get("/agent")
def agent():
    return {
        "agent_response": "Task processed by AI Agent"
    }
