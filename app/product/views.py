from typing import List
from fastapi import APIRouter, HTTPException, status, Depends

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from product.models import Product
from product.schemas import ProductSchema


engine = create_engine("postgresql://postgres:090205@localhost/fastapi1_db")
SesssionLocal = sessionmaker(bind=engine)

def get_db():
    db = SesssionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix='/api')

@router.get("/products/", response_model=List[ProductSchema], status_code=status.HTTP_200_OK)
async def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@router.post("/products/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(data: ProductSchema, db: Session = Depends(get_db)):
    product = Product(**data.dict())
    print(product)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/products/{id}/", response_model=ProductSchema, status_code=status.HTTP_200_OK)
async def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id==id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Мындай товар жок!")
    return product


@router.put("/products/{id}/", response_model=ProductSchema, status_code=status.HTTP_200_OK)
async def update_product(id: int, name:str=None, price:float=None, description:str=None,   db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id==id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Мындай товар жок!")
    
    if name:
        product.name = name
    if  price:
        product.price = price
    if description:
        product.description = description
    db.commit()
    db.refresh(product)
    return product


@router.delete("/products/{name}/",  status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(name: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.name==name).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Мындай продукт жок!")

    db.delete(product)
    db.commit()
    return {"detail": "Удален"}
   

