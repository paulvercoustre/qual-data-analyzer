from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Import CORS Middleware

# Import routers
from app.routers import auth

app = FastAPI(title="QDAS Backend")

# CORS Configuration
origins = [
    "http://localhost:5173", # Default Vite dev server port
    "http://localhost:3000", # Default Create React App dev server port
    # Add any other origins (e.g., your production frontend URL) here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # List of allowed origins
    allow_credentials=True, # Allow cookies
    allow_methods=["*"], # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"], # Allow all headers
)

# Include routers
app.include_router(auth.router, prefix="/auth")

@app.get("/")
async def read_root():
    return {"message": "QDAS Backend is running"}

# Add other endpoints and logic here later 