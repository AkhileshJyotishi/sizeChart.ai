from fastapi import FastAPI

from services.size_chart_service import initialzeInmemoryDatabase 
from fastapi.middleware.cors import CORSMiddleware
initialzeInmemoryDatabase()

app = FastAPI()
# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Replace with specific origins if needed.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods.
    allow_headers=["*"],  # Allows all headers.
)

from routers.size_chart import router as size_chart_router
# from routers.feedback import router as feedback_router


app.include_router(size_chart_router, prefix="/size-chart", tags=["Size Chart"])
# app.include_router(feedback_router, prefix="/feedback", tags=["Feedback"])
