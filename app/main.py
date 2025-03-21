from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.database import mongodb
from app.api.routes import branches, categories, menu, franchise, job_positions, job_applications,gallery_cat,image,online_order_link,testimonial

# Initialize FastAPI
app = FastAPI(title="Banjo's Restaurant API")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change this in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)
# Serve static files (e.g., images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(branches.router, prefix="/branches", tags=["Branches"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(menu.router, prefix="/menu", tags=["Menu"])
app.include_router(franchise.router, prefix="/franchise", tags=["Franchise"])
app.include_router(job_positions.router, prefix="/job-positions", tags=["Job Positions"])
app.include_router(job_applications.router, prefix="/job-applications", tags=["Job Applications"])
app.include_router(gallery_cat.router,prefix="/gallery_cat", tags=["Gallery cat"])
app.include_router(image.router,prefix="/images", tags=["Image"])
app.include_router(online_order_link.router, prefix="/api/online-order-links", tags=["Online Order Links"])
app.include_router(testimonial.router, prefix="/testimonial", tags=["Testimonial"])

# Lifecycle events for database connection
@app.on_event("startup")
async def startup_db():
    """Connect to MongoDB on application startup."""
    await mongodb.connect()

@app.on_event("shutdown")
async def shutdown_db():
    """Disconnect from MongoDB on application shutdown."""
    await mongodb.close()

# Root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to Banjo's Restaurant API"}