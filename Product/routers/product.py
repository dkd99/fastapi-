from fastapi import APIRouter
from sqlalchemy.orm import Session
from Product.routers.login import get_current_user
from fastapi.params import Depends
from ..database import get_db
from .. import models,schemas
from typing import List
from fastapi import FastAPI,Response,HTTPException
from fastapi import status

router = APIRouter(tags=['Products'])

@router.get('/products',response_model = List[schemas.DisplayProduct])
def products(db: Session = Depends(get_db),current_user:schemas.Seller = Depends(get_current_user)):
    products = db.query(models.Product).all()#.filter(models.Product.id== id).first()
    return products

@router.get('/product/{id}',response_model = schemas.DisplayProduct)
def products(id,response:Response,db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id== id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,details='Product not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'Product not found'}
    return product

@router.delete('/product/{id}')
def delete(id,db: Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id== id).delete(synchronize_session=False)
    return {f'product with id {id} deleted'}

@router.put('/product/{id}')
def update(id,request: schemas.Product,db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id== id)
    if not product:
        pass
    
    product.update(request.dict())
    db.commit()
    return {'Product Updated Successfully'}
@router.post('/product',status_code=status.HTTP_201_CREATED)
def add(request: schemas.Product,db: Session = Depends(get_db)):
    new_product = models.Product(name=request.name,description=request.description,price=request.price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request