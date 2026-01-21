from fastapi import FastAPI

app = FastAPI(title="DraftForge")

@app.get("/")
def check():
    return {"status": "DraftForge is running!"}