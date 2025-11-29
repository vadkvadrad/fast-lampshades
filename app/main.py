from fastapi import FastAPI
from app.api import auth, products, cart, orders
from app.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    Base.metadata.create_all(bind=engine)
    yield
    # Cleanup on shutdown if needed
    pass

app = FastAPI(
    title="LampShades MVP API", 
    description="Simple e-commerce API for lamp shades", 
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to LampShades MVP API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}