from fastapi import FastAPI

app = FastAPI(title="QDAS Backend")

@app.get("/")
async def read_root():
    return {"message": "QDAS Backend is running"}

# Add other endpoints and logic here later 