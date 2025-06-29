from fastapi import FastAPI,Response,HTTPException
from fastapi.params import Depends
from sqlalchemy.sql.functions import mode
from sqlalchemy.orm import Session
from fastapi import status
from . import schemas
from . import models
from .database import engine,SessionLocal
from typing import List

app =FastAPI()
models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield 
    finally:
        db.close()
        
@app.get('/products',response_model = List[schemas.DisplayProduct])
def products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()#.filter(models.Product.id== id).first()
    return products

@app.get('/product/{id}',response_model = schemas.DisplayProduct)
def products(id,response:Response,db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id== id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,details='Product not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'Product not found'}
    return product

@app.delete('/product/{id}')
def delete(id,db: Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id== id).delete(synchronize_session=False)
    return {f'product with id {id} deleted'}

@app.put('/product/{id}')
def update(id,request: schemas.Product,db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id== id)
    if not product:
        pass
    
    product.update(request.dict())
    db.commit()
    return {'Product Updated Successfully'}
@app.post('/product',status_code=status.HTTP_201_CREATED)
def add(request: schemas.Product,db: Session = Depends(get_db)):
    new_product = models.Product(name=request.name,description=request.description,price=request.price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request
    