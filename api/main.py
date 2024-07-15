from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import models
from .dependencies.database import engine
from .controllers import orders, sandwiches, resources, recipes, order_details

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Sandwich Maker API!"}

# Include routers for different tables
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(sandwiches.router, prefix="/sandwiches", tags=["Sandwiches"])
app.include_router(resources.router, prefix="/resources", tags=["Resources"])
app.include_router(recipes.router, prefix="/recipes", tags=["Recipes"])
app.include_router(order_details.router, prefix="/order_details", tags=["Order Details"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
