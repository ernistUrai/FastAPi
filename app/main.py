from fastapi import FastAPI
from product.views import router, engine
from product.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)