from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.init import initialize_db
from campaigns.router import router as campaigns_router
from auth.router import router as auth_router

# Run the init function to ensure the database is ready.
initialize_db()

app = FastAPI(title="Backend API", version="1.0.0")

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Backend API is running"}

# Authentication routes
app.include_router(auth_router)
# Campaign-related routes
app.include_router(campaigns_router)